from flask_wtf import FlaskForm # type: ignore
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired # type: ignore


class formCalculadora(FlaskForm) :
    num1 = IntegerField('Numero1', validators=[DataRequired('Tienes que introducir el dato')])
    num2 = IntegerField('Numero2', validators=[DataRequired('Tienes que introducir el dato')])
    operador = SelectField('Operador', choices=[('+', 'Sumar'), ('-', 'Restar'), ('*', 'Multiplicar'), ('/', 'Dividir')])

    submit = SubmitField('Submit')

class uploadForm(FlaskForm) :
    photo = FileField('Selecciona imagne: ', validators=[FileRequired()])
    submit = SubmitField('Submit')