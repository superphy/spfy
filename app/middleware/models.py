import sys
import copy
import config
import redis
import cPickle as pickle
from hashlib import sha1
from dis import dis
from StringIO import StringIO
from jsonmodels import models, fields
from middleware.graphers.turtle_utils import actual_filename

def _convert_model(model):
    # Convert the model to a generic JSON structure.
    struct = model.to_struct()
    if 'rows' in struct:
        # This is not strictly json; more like a list than a dict structure.
        rows_list = struct['rows']
        return rows_list
    else:
        return struct

def model_to_json(model):
    """
    Converts models to json for the front-end.
    """
    # Validate the model submitted before processing.
    model.validate()
    # Conversion.
    if isinstance(model, models.Base):
        return _convert_model(model)
    else:
        raise Exception('model_to_json() called for a model without a handler.')


class SubtypingRow(models.Base):
    analysis = fields.StringField(required=True)
    contigid = fields.StringField(required=True)
    filename = fields.StringField(required=True)
    hitcutoff = fields.StringField(nullable=True)
    hitname = fields.StringField(required=True)
    hitorientation = fields.StringField(nullable=True)
    hitstart = fields.StringField(nullable=True)
    hitstop = fields.StringField(nullable=True)


class SubtypingResult(models.Base):
    rows = fields.ListField([SubtypingRow], nullable=True)

class PhylotyperRow(models.Base):
    contig = fields.StringField(nullable=True)
    genome = fields.StringField()
    probability = fields.StringField(nullable=True) # actually float
    start = fields.StringField(nullable=True) # actually int
    stop = fields.StringField(nullable=True) # actually int
    subtype = fields.StringField()
    subtype_gene = fields.StringField(nullable=True)

class PhylotyperResult(models.Base):
    rows = fields.ListField([PhylotyperRow], nullable=True)

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
        self.cache += [copy.deepcopy(self.jobs)]
        self.jobs = {}

    def merge_jobs(self):
        """
        
        """
        # If the jobs dictionary is not empty.
        if self.jobs:
            self.cache_jobs()
        # Actual merge. Notice were converting to list.
        self.final_jobs = [
            j
            for d in self.cache
            for j in d.values()
        ]

    def complete(self):
        """
        Check if all jobs are completed
        """
        for j in self.final_jobs:
            # Type check.
            assert isinstance(j, Job)
            rq_job = j.rq_job
            if j.backlog:
                # Some backlog job, we don't care (though Sentry will catch it).
                continue
            elif rq_job.is_failed:
                # If the job failed, return the error.
                return rq_job.exc_info
            elif not rq_job.is_finished:
                # One of the jobs hasn't finished.
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
            j.rq_job for j in self.final_jobs
            if j.display and j.rq_job.is_finished and not j.rq_job.is_failed
        ]
        # Merge the json lists together.
        l = []
        for rq_job in completed_jobs:
            model = rq_job.result
            list_json = model_to_json(model)
            l += list_json
        return l

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

    def store(self):
        """
        Stores the pipeline (via Pickle) to Redis DB and creates a pipeline id for return.
        :param pipeline: An instance of the models.Pipeline class.
        :return: (dict): {"pipeline..." id: "Subtyping"}
        """
        pipeline_id = "pipeline{0}".format(self.sig)

        # Start a Redis connection.
        redis_url = config['REDIS_URL']
        redis_connection = redis.from_url(redis_url)

        # Store the pipeline instance.
        redis_connection.set(pipeline_id, pickle.dumps(self))

        # Create a similar structure to the old return
        d = {}
        d[pipeline_id] = {}
        d[pipeline_id]['analysis'] = "Subtyping"

        d[pipeline_id]['file'] = self.files
        print '_store_pipeline(): finished'
        return d
