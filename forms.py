from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, InputRequired, Length


class EncryptForm(FlaskForm):
    text = TextAreaField("Message to BeanKrypt", validators=[DataRequired(), Length(min=1, max=3735)])
    bean_type = RadioField("Bean Type", choices=['Baked','Black','Pinto'], validators=[DataRequired()])
    submit = SubmitField('BeanKrypt Message')


class DecryptForm(FlaskForm):
    image = FileField('Image to Un-BeanKrypt', validators=[InputRequired(), FileAllowed(['png'], 'PNG only')])
    submit = SubmitField('Un-BeanKrypt Image')