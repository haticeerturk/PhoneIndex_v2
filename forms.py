from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class RecordForm(FlaskForm):
    name = StringField('Ad: ', validators=[DataRequired()])
    surname = StringField('Soyad: ', validators=[DataRequired()])
    phone_number = StringField('Telefon Numarası: ', validators=[DataRequired()])
