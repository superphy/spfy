import sys
import copy
import config
import redis
import dill
from hashlib import sha1
from dis import dis
from StringIO import StringIO
from jsonmodels import models, fields
from flask import jsonify
from middleware.graphers.turtle_utils import actual_filename

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
    # Validate the model submitted before processing.
    assert isinstance(model, list)
    # model.validate()
    # Conversion.
    print("model_to_json() called with model: {0}".format(str(model)))
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
    print '_store_pipeline(): finished'
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

class Pipeline():
    def __init__(self, jobs=None, files=None, func=None, options=None):
        if not jobs:
            jobs = {}
        if not files:
            files = []
        if not options:
            options = {}
        self.jobs = {} # {'somename': instance of RQ.Job} Only used when enqueing.
        self.final_jobs = [] # Jobs for every file in the request.
        self.cache = [] # For temporary storage of RQ.Jobs.
        self.sig = None
        self.files = []
        self.func = func # Additional attribute for storing pipeline function.
        self.options = options
        self.signature() # Create & Store a signature for the pipeline.

    def cache_jobs(self):
        """
        Copy current jobs to cache.
        """
        self.cache += [self.jobs]
        self.jobs = {}

    def merge_jobs(self):
        """

        """
        # If the jobs dictionary is not empty.
        if self.jobs:
            self.cache_jobs()
        # Actual merge. Notice were converting to list.
        self.final_jobs = [
            j # Where j is our custom Job class, not an rq_job
            for d in self.cache
            for j in d.values()
        ]

    def complete(self):
        """
        Check if all jobs are completed
        """
        print("complete() checking status for: {0}".format(str(self.final_jobs)))
        for j in self.final_jobs:
            # Type check.
            assert isinstance(j, Job)
            rq_job = j.rq_job
            if j.backlog:
                # Some backlog job, we don't care (though Sentry will catch it).
                print("complete(): job {0} is in backlog.".format(j.name))
                continue
            elif rq_job.is_failed:
                # If the job failed, return the error.
                print("complete(): job {0} is failed with exc_info {1}.".format(j.name, rq_job.exc_info))
                return rq_job.exc_info
            elif not rq_job.is_finished:
                # One of the jobs hasn't finished.
                print("complete(): job {0} is finished.".format(j.name))
                return False
        return True

    def to_json(self):
        """
        Reduces all results from self.jobs to json for return. Note: currently
        using a list as this is what the front-end is expecting, but convert
        to dict a some point.
        """
        # Gather all the jobs that have finished and haven't failed.
        completed_jobs = [
            j for j in self.final_jobs
            if j.display and not j.backlog and j.rq_job.is_finished and not j.rq_job.is_failed
        ]
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