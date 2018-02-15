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

class Pipeline(models.Base):
    jobs = {}
    single_dict = fields.EmbeddedField(dict, default={})
