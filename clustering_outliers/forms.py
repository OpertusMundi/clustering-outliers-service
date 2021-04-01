from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, FieldList
from wtforms.validators import DataRequired, AnyOf, Optional


RESPONSE_ERROR_INPUT_MESSAGE = "Permitted values for response are prompt or deferred"
RESOURCE_TYPE_ERROR_INPUT_MESSAGE = "Permitted values for response are prompt or deferred"


class BaseKMeansForm(FlaskForm):
    resource_type = StringField('resource_type', validators=[DataRequired(),
                                                             AnyOf(['csv', 'shp'], RESPONSE_ERROR_INPUT_MESSAGE)])
    response = StringField('response',
                           validators=[Optional(), AnyOf(['prompt', 'deferred'], RESPONSE_ERROR_INPUT_MESSAGE)],
                           default='prompt')
    columns = FieldList(StringField('columns', validators=[Optional()], default=[]),
                        min_entries=0, validators=[Optional()])
    k = IntegerField('k', validators=[Optional()])
    dist_measure = StringField('dist_measure', validators=[Optional()], default='euclidean')

    id_column_name = StringField('id_column_name', validators=[Optional()])
    column_names = FieldList(StringField('column_names', validators=[Optional()], default=[]),
                             min_entries=0, validators=[Optional()])
    id_column_number = StringField('id_column_number', validators=[Optional()])
    column_numbers = FieldList(StringField('column_numbers', validators=[Optional()], default=[]),
                               min_entries=0, validators=[Optional()])

    class Meta:
        csrf = False


class KMeansFileForm(BaseKMeansForm):
    resource = FileField('resource', validators=[DataRequired()])


class KMeansPathForm(BaseKMeansForm):
    resource = StringField('resource', validators=[DataRequired()])
