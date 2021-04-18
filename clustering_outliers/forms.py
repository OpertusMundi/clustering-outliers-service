from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, FieldList, FloatField
from wtforms.validators import DataRequired, AnyOf, Optional


RESPONSE_ERROR_INPUT_MESSAGE = "Permitted values for response are prompt or deferred"
RESOURCE_TYPE_ERROR_INPUT_MESSAGE = "Permitted values for response are prompt or deferred"


class BaseForm(FlaskForm):
    resource_type = StringField('resource_type', validators=[DataRequired(),
                                                             AnyOf(['csv', 'shp'], RESPONSE_ERROR_INPUT_MESSAGE)])
    response = StringField('response',
                           validators=[Optional(), AnyOf(['prompt', 'deferred'], RESPONSE_ERROR_INPUT_MESSAGE)],
                           default='prompt')

    columns = FieldList(StringField('columns', validators=[Optional()], default=[]),
                        min_entries=0, validators=[Optional()])
    id_column = StringField('id_column', validators=[Optional()])

    class Meta:
        csrf = False


class BaseOCSVMForm(BaseForm):
    degree = IntegerField('degree', validators=[Optional()])


class BaseLOFForm(BaseForm):
    n_neighbors = IntegerField('n_neighbors', validators=[Optional()])


class BaseIsoForestForm(BaseForm):
    n_estimators = IntegerField('n_estimators', validators=[Optional()])
    max_samples = IntegerField('max_samples', validators=[Optional()])


class BaseAgglomerativeForm(BaseForm):
    k = IntegerField('k', validators=[Optional()])
    linkage = StringField('linkage', validators=[Optional(), AnyOf(['ward', 'complete', 'average', 'single'],
                                                                   "Valid linkage options are: 'ward', 'complete', 'average', 'single'")])
    dist_threshold = FloatField('dist_threshold', validators=[Optional()])
    dist_measure = StringField('dist_measure', validators=[Optional()], default='euclidean')


class BaseDBScanForm(BaseForm):
    epsilon = FloatField('epsilon', validators=[Optional()])
    min_samples = IntegerField('min_samples', validators=[Optional()])
    dist_measure = StringField('dist_measure', validators=[Optional()], default='euclidean')


class BaseKMeansForm(BaseForm):
    k = IntegerField('k', validators=[Optional()])
    dist_measure = StringField('dist_measure', validators=[Optional()], default='euclidean')


class OCSVMFileForm(BaseOCSVMForm):
    resource = FileField('resource', validators=[DataRequired()])


class OCSVMPathForm(BaseOCSVMForm):
    resource = StringField('resource', validators=[DataRequired()])


class LOFFileForm(BaseLOFForm):
    resource = FileField('resource', validators=[DataRequired()])


class LOFPathForm(BaseLOFForm):
    resource = StringField('resource', validators=[DataRequired()])


class IsoForestFileForm(BaseIsoForestForm):
    resource = FileField('resource', validators=[DataRequired()])


class IsoForestPathForm(BaseIsoForestForm):
    resource = StringField('resource', validators=[DataRequired()])


class AgglomerativeFileForm(BaseAgglomerativeForm):
    resource = FileField('resource', validators=[DataRequired()])


class AgglomerativePathForm(BaseAgglomerativeForm):
    resource = StringField('resource', validators=[DataRequired()])


class DBScanFileForm(BaseDBScanForm):
    resource = FileField('resource', validators=[DataRequired()])


class DBScanPathForm(BaseDBScanForm):
    resource = StringField('resource', validators=[DataRequired()])


class KMeansFileForm(BaseKMeansForm):
    resource = FileField('resource', validators=[DataRequired()])


class KMeansPathForm(BaseKMeansForm):
    resource = StringField('resource', validators=[DataRequired()])
