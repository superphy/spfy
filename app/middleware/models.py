import sys
from hashlib import sha1
from dis import dis
from StringIO import StringIO
from jsonmodels import models, fields
from middleware.graphers.turtle_utils import actual_filename

def _convert_subtyping(model):
    # Convert the model to a generic JSON structure.
    struct = model.to_struct()
    # This is not strictly json; more like a list than a dict structure.
    rows_list = struct['rows']
    return rows_list

def model_to_json(model):
    """
    Converts models to json for the front-end.
    """
    # Validate the model submitted before processing.
    model.validate()
    # Conversion.
    if isinstance(model, SubtypingResult):
        return _convert_subtyping(model)
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
        self.jobs = {} # {'somename': instance of RQ.Job}
        self.sig = None # Signtaure isn't generated until necessary
        # TODO: incorporate below into the pipeline.
        self.files = []
        self.func = func # Additional attribute for storing pipeline function.
        self.options = options

    def complete(self):
        """
        Check if all jobs are completed
        """
        for j in self.jobs.itervalues():
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
        Reduces all results from self.jobs to json for return.
        """
        # Gather all the jobs that have finished and haven't failed.
        completed_jobs = [
            j.rq_job for j in self.jobs.itervalues()
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
