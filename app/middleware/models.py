import sys
import traceback
import config
import redis
import dill
from hashlib import sha1
from dis import dis
from StringIO import StringIO
from jsonmodels import models, fields
from flask import jsonify
from datetime import datetime
from middleware.graphers.turtle_utils import actual_filename
from routes.job_utils import fetch_job

# def _convert_model(model):
#     # Convert the model to a generic JSON structure.
#     struct = model.to_struct()
#     # Check that struct isn't empty.
#     assert struct
#     if 'rows' in struct:
#         # This is not strictly json; more like a list than a dict structure.
#         rows_list = struct['rows']
#         return rows_list
#     else:
#         return struct

def model_to_json(model):
    """
    Converts models to json for the front-end.
    """
    #TODO: can access the list directly, no longer need this.
    # Validate the model submitted before processing.
    assert isinstance(model, list)
    # model.validate()
    # Conversion.
    # print("model_to_json() called with model: {0}".format(str(model)))
    return model
    # if isinstance(model, models.Base):
    #     return _convert_model(model)
    # else:
    #     raise Exception('model_to_json() called for a model without a handler.')

def store(pipeline):
    """
    Stores the pipeline (via Pickle) to Redis DB and creates a pipeline id for return.
    :param pipeline: An instance of the models.Pipeline class.
    :return: (dict): {"pipeline..." id: "Subtyping"}
    """
    assert isinstance(pipeline, Pipeline)
    pipeline_id = "pipeline{0}".format(pipeline.sig)

    # Start a Redis connection.
    redis_url = config.REDIS_URL
    redis_connection = redis.from_url(redis_url)

    # Store the pipeline instance.
    redis_connection.set(pipeline_id, dill.dumps(pipeline))

    # Create a similar structure to the old return
    d = {}
    d[pipeline_id] = {}
    d[pipeline_id]['analysis'] = "Subtyping"

    d[pipeline_id]['file'] = pipeline.files
    print('_store_pipeline(): storing pipeline with id {0} containing {1} # of files with {2} # of final jobs has finished.'.format(pipeline.sig, len(pipeline.files), len(pipeline.final_jobs)))
    return d

def load(pipeline_id):
    """
    Must load Pipeline instances with this function, as a pickle.loads() needs
    access to the Pipeline class definition to correctly load it.
    :param pipeline_id:
    :return:
    """
    # Start a Redis connection.
    redis_url = config.REDIS_URL
    redis_connection = redis.from_url(redis_url)

    # Get the pipeline instance.
    raw = redis_connection.get(pipeline_id)
    pipeline = dill.loads(raw)
    assert isinstance(pipeline, Pipeline)
    return pipeline

def unpickle(pickled_file):
    """
    Define a function for unpickling. Should address issues with unpickling custom classes.
    :param pickled_file:
    :return:
    """
    unpickled = dill.load(open(pickled_file, 'rb'))
    assert isinstance(unpickled, (models.Base, Pipeline, dict, list))
    return unpickled

def dump(obj, path):
    dill.dump(obj, open(path, 'wb'))

class SubtypingRow(models.Base):
    def __init__(self, analysis="", contigid="", filename="", hitcutoff="", hitname="", hitorientation="", hitstart="",hitstop=""):
        self.analysis = analysis
        self.contigid = contigid
        self.filename = filename
        self.hitcutoff = hitcutoff
        self.hitname = hitname
        self.hitorientation = hitorientation
        self.hitstart = hitstart
        self.hitstop = hitstop


class SubtypingResult(models.Base):
    def __init__(self, rows=None):
        if not rows:
            rows = []
        self.rows = rows

class PhylotyperRow(models.Base):
    def __init__(self):
        self.contig = fields.StringField(nullable=True)
        self.genome = fields.StringField()
        self.probability = fields.StringField(nullable=True) # actually float
        self.start = fields.StringField(nullable=True) # actually int
        self.stop = fields.StringField(nullable=True) # actually int
        self.subtype = fields.StringField()
        self.subtype_gene = fields.StringField(nullable=True)

class PhylotyperResult(models.Base):
    def __init__(self):
        self.rows = fields.ListField([PhylotyperRow], nullable=True)


class Job():
    def __init__(self, rq_job, name="", transitory=True, backlog=True, display=False):
        """
        Args:
            rq_job: An instance of the RQ Job class.
            transitory: Some intermediate, we only care if it failed. It's ok
                if the job isn't found in Redis.
            backlog: For background processing, we don't care whatsoever. Will
                still be caught by Sentry.io if it fails.
            display: To per parsed for the front-end.
        """
        self.rq_job = rq_job
        self.name = name
        self.transitory = transitory
        self.backlog = backlog
        self.display = display
        self.times = None

    def refetch(self):
        if self.times:
            # If timings exist, the job is done. Don't refetch.
            pass
        elif self.rq_job.exc_info == 'job not found':
            # If called on a job who's result_ttl has elapsed.
            print('model.Job.refetch(): job {0} was already determined to not be found.'.format(self.name))
        else:
            # Start a Redis connection.
            redis_url = config.REDIS_URL
            redis_connection = redis.from_url(redis_url)

            # While you can call rq_job.result without refetching, you must refetch
            # do get the start and stop times.
            job = fetch_job(self.rq_job.get_id(), redis_connection)
            self.rq_job = job

    def time(self):
        # Only necessary if called from Pipeline.cache.
        if not self.times:
            self.refetch()

        # If we've already saved the timings.
        if self.times:
            return self.times
        elif self.rq_job.exc_info == 'job not found':
            # If called on a job who's result_ttl has elapsed.
            # Should only ever see this called once per job.
            print('model.Job.time(): job {0} could not be found.'.format(self.name))
            self.times = (0,0,0)
            return self.times
        elif not self.rq_job.is_finished:
            # Should never see this.
            print('model.Job.time(): time was called for an unfinished job named {0} of type {1} with content {2}'.format(self.name, type(self.rq_job), self.rq_job))
            return (-1,-1,-1)
        else:
            try:
                job = self.rq_job
                assert job.is_finished
                start = job.started_at
                stop = job.ended_at
                timedelta = stop - start
                sec = timedelta.total_seconds()
                self.times = (start,stop,sec)
                return (start,stop,sec)
            except Exception, e:
                # Try and grab the traceback.
                # This doesn't really happen do to above tests beforehand.
                try:
                    exc_info = sys.exc_info()
                finally:
                    print('model.Job.time(): could not calculate time for {0} of type {1} with content {2}'.format(self.name, type(self.rq_job), self.rq_job))
                    traceback.print_exception(*exc_info)
                    del exc_info
                self.times = (0,0,0)
                return self.times

class Pipeline():
    def __init__(self, jobs=None, files=None, func=None, options=None, date=None):
        if not jobs:
            jobs = {}
        if not files:
            files = []
        if not options:
            options = {}
        if not date:
            now = datetime.now()
            now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
            date = now
        self.jobs = {} # {'somename': instance of RQ.Job} Only used when enqueing.
        self.final_jobs = {} # Jobs for every file in the request.
        self.cache = [] # For temporary storage of RQ.Jobs.
        self.sig = None
        self.files = []
        self.func = func # Additional attribute for storing pipeline function.
        self.options = options
        self.signature() # Create & Store a signature for the pipeline.
        self.date = date
        self.done = False # Bypass for the self.complete() method.

    def cache_jobs(self, filename):
        """
        Copy current jobs to cache. Called on every iteration of a file.
        """
        self.cache += [{filename:self.jobs}]
        self.jobs = {}

    def merge_jobs(self, drop=True):
        """Merges all the jobs into a self.final_jobs of form {filename:[models.Job]}.
        """
        # If the jobs dictionary is not empty.
        if self.jobs:
            raise Exception('models.Pipeline.merge_jobs(): called before caching all jobs.')

        for outer_d in self.cache:
            new_l = []
            # {filename: {(str)func: Job}} should only have 1 inner dict/filename.
            assert len(outer_d.keys()) == 1
            assert len(outer_d.values()) == 1
            filename = outer_d.keys()[0]
            inner_d = outer_d.values()[0]
            # Gather the models.Job instances.
            for j in inner_d.values():
                if not drop:
                    new_l.append(j)
                elif drop and not j.backlog:
                    new_l.append(j)
            self.final_jobs.update({filename:new_l})
        ret = { f:len(l) for f,l in self.final_jobs.items() }
        print("merge_jobs(): merged with {0}.".format(ret))

    def refetch(self):
        '''Refetch method for the Pipeline class. Removes jobs that are finished
        and can no longer be found. Also updates itself on Redis DB.
        '''
        # new_finals = []
        for j in self.final_jobs.values():
            j.refetch()
            # if not j.rq_job.exc_info == 'job not found':
            #     new_finals.append(j)
        # self.final_jobs = new_finals

    def complete(self):
        """
        Check if all jobs are completed
        """
        if self.done:
            return True
        else:
            print("complete() checking status for: {0} with {1} # of final jobs.".format(self.sig, len(self.final_jobs.values())))
            self.refetch()
            for j in self.final_jobs.values():
                # Type check.
                assert isinstance(j, Job)
                rq_job = j.rq_job
                if j.times:
                    # We've checked this before and its complete.
                    continue
                elif j.backlog:
                    # Some backlog job, we don't care (though Sentry will catch it).
                    # This doesn't really get called due to dropping backlog by default.
                    continue
                elif rq_job.exc_info == 'job not found':
                    # Job finished, but the result_ttl timed out.
                    print("complete(): job {0} is finished but the result_ttl timed out.".format(j.name))
                    continue
                elif rq_job.is_failed:
                    # If the job failed, return the error.
                    # Failed jobs last forever (result_ttl=-1) in RQ.
                    print("complete(): job {0} is failed with exc_info {1}.".format(j.name, rq_job.exc_info))
                    return rq_job.exc_info
                elif not j.transitory and not rq_job.is_finished:
                    # One of the jobs hasn't finished.
                    # The only reason this works is that there's always a non-
                    # transitory job to be run after w/e this job is.
                    print("complete(): job {0} is still pending with var: {1}.".format(j.name, rq_job.is_finished))
                    return False
                elif rq_job.is_finished and not j.times:
                    # The job is done, save timings.
                    print("complete(): saving timing for job {0}.".format(j.name))
                    j.time()
                elif j.transitory and rq_job.is_finished:
                    # Some of the elif is extra, but checks that this is
                    # a transitory job that is finished.
                    print("complete(): job {0} is j.transitory and rq_job.is_finished.".format(j.name))
                    continue
            print("complete(): pipeline {0} is complete.".format(self.sig))
            # Pipeline complete.
            self.done = True
            store(self)
            return True

    def timings(self):
        '''Looks through Pipeline.final_jobs and return timings, also finds the
        overall runtime from start to finish.
        '''
        assert self.done
        # l is the actual return list.
        l = [{'{0}|{1}'.format(f,j.name): j.time()} for f,j in self.final_jobs.items()]
        # Sanity check.
        assert len(l) == len(self.final_jobs.values())
        # Tabulate starts and stops.
        starts = [i.values()[0][0] for i in l if i.values()[0][0]]
        stops = [i.values()[0][1] for i in l if i.values()[0][1]]
        # Calculate min/max datetime.date values.
        mn = starts[0]
        for i in starts:
            if i < mn:
                mn = i
        mx = stops[0]
        for i in stops:
            if i > mx:
                mx = i
        # Append total runtime.
        sec = (mx-mn).total_seconds()
        l.append({'total': (mn,mx,sec)})
        return l

    def _completed_jobs(self):
        '''Returns jobs that are required for frontend and are complete.
        '''
        completed_jobs = [
            j for j in self.final_jobs.values()
            if j.display and not j.backlog and j.rq_job.is_finished and not j.rq_job.is_failed
        ]
        return completed_jobs

    def to_json(self):
        """
        Reduces all results from self.jobs to json for return. Note: currently
        using a list as this is what the front-end is expecting, but convert
        to dict a some point.
        """
        # Gather all the jobs that have finished and haven't failed.
        completed_jobs = self._completed_jobs()
        print("to_json() completed_jobs: {0}".format(str(completed_jobs)))
        # Merge the json lists together.
        l = []
        for j in completed_jobs:
            rq_job = j.rq_job
            model = rq_job.result
            try:
                # TODO: This is not correct as while the new ECTYper call does return a model, the display_subtyping() call that the return job is associated with will already convert the result to a list and return it.
                assert isinstance(model, (models.Base,list))
            except:
                raise Exception("to_json() called for job {0}  with result of type {1} and info {2}".format(j.name, type(model), str(model)))
            list_json = model_to_json(model)
            l += list_json
        return jsonify(l)

    def _function_signature(self):
        """
        Generates signatures for functions.
        """
        # dis.dis() sends output to stdout, we need to capture it to generate
        # a signature.

        # Assign the old stdout.
        old_stdout = sys.stdout
        # Create a buffer for the new output.
        result = StringIO()
        # Swap the stdout to our buffer.
        sys.stdout = result
        # dis() call.
        dis(self.func)
        # Restore the stdout to screen.
        sys.stdout = old_stdout
        # Grab the output from the dis() call.
        result_string = result.getvalue()
        return result_string

    def signature(self):
        """
        Create a signature that can identify a given task. Used to check
        if the same task was requested.
        """
        # Create a string of the function signature.
        str_func = self._function_signature()
        # Start the hashing process with the function signature.
        hx = sha1(str_func)

        # Create a string of the files.
        str_files = str(self.files)
        # Update the hash with our args information.
        hx.update(str_files)

        # Create a string of the options.
        str_options = str(self.options)
        # Update the hash with our args information.
        hx.update(str_options)

        # Use the hexdigest as the signature.
        sig = hx.hexdigest()
        self.sig = sig
        return sig
