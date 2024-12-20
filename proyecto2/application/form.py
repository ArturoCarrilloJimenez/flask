from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, NumberRange
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

class formSiNo(FlaskForm) :
    si = SubmitField('Si')
    no = SubmitField('No')

class LoginForm(FlaskForm) :
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class formUser(FlaskForm) :
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class formChangePassword(FlaskForm) :
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Aceptar')

class formCarrrito(FlaskForm) :
    id = HiddenField()
    cantidad =  IntegerField('Cantidad', default=1, validators=[NumberRange(min=1, message='Debes de ingresar un numero positivo'), DataRequired('Tienes que introducir el dato')])
    submit = SubmitField('Aceptar')