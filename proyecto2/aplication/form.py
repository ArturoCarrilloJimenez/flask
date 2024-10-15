from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

class formArticulos(FlaskForm) :
    nombre = StringField('Nombre: ', validators=[DataRequired('Tienes que introducir el dato')])
    precio = DecimalField('Precio:', default=0, validators=[DataRequired('Tienes que introducir el dato')])
    iva = IntegerField('IVA: ', default=0, validators=[DataRequired('Tienes que introducir el dato')])
    descripcion = TextAreaField('Descripcion: ')
    photo = FileField('Selecciona imagen: ')
    stock = IntegerField('Stock: ', default=1, validators=[DataRequired('Tienes que introducir el dato')])
    CategoriaId = SelectField('Categoria', coerce=int)
    submit = SubmitField('Enviar')
class formCategorias(FlaskForm) :
    nombre = StringField('Nombre: ', validators=[DataRequired('Tienes que introducir el dato')])
    submit = SubmitField('Enviar')