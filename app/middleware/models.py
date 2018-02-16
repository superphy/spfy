from jsonmodels import models, fields


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
    def __init__(self, job, transitory=True, display=False):
        self.job = job # an instance of the RQ Job class
        self.transitory = # if the job won't persist in Redis DB
        self.display = # used for display to the front-end
        
class Pipeline():
    def __init__(self, jobs=None, single_dict=None):
        if not jobs:
            jobs = {}
        if not single_dict:
            single_dict = {}
        self.jobs = {}
        self.single_dict = {}
