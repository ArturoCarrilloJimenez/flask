from flask import Flask, request, make_response, abort, redirect, url_for, render_template
from flask_bootstrap import Bootstrap5
from aplicacion.forms import formCalculadora, uploadForm
from werkzeug.utils import secure_filename
from os import listdir

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = 'text aleatorio dndewidunai'

# Enrutaminento con flask
@app.route('/')
def hello_word():
    return '<h1>Hello, Word!</h1>'

# Ruta con id y el metodo get
@app.route('/id=<int:id>',methods=['GET'])
def mostrarId(id) :
    return '<h1>Pagina con el id: {}'.format(id),'</h1>'

# Ruta que concadena rutas y despues segun el caso muestra un contenido distisnto
@app.route('/hello')
@app.route('/hello/<string:name>')
@app.route('/hello/<string:name>/<int:edad>')
def hello(name=None, edad=None) :
    if name and edad :
        return ' {0}, tienes {1} años'.format(name, edad)
    elif name :
        return 'Hola {0}'.format(name)
    else :
        return 'Hola';

# Metodo de tipo POST
@app.route('/article', methods=['POST'])
def article() :
    return 'Articulo por metodo POST'

# Metodo de tipo GET o POST, segun cual sea escogera uno o otro
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Metodo POST'
    else :
        return 'Metodo GET'

# Ruta que muestra un form al utilizar el metodo get, una vez enviado utilizara el metodo post
@app.route('/suma', methods=['GET', 'POST'])
def sumar() :
    if request.method == 'POST': # Metodo de tipo post
        num1=request.form.get('num1')
        num2=request.form.get('num2')
        return str(int(num1) + int(num2))
    else : # Metodo de tipo get
        return '''<form action="/suma"
        method="POST">
            <label>N1</label>
            <input type="text" name="num1"></input>
            <label>N2</label>
            <input type="text" name="num2"></input>
            <input type="submit"/>
        </form>'''

@app.route('/object/')
def return_object() :
    headers = {'Content.Type' : 'text/plain'}
    return make_response('Hello, world!', 200, headers)

# Una tupla es un array inmutable, es decir, no se puede modificar
@app.route('/tuple/')
def return_tuple() :
    return make_response('Hello, world!', 200, {'Content.Type' : 'text/plain'});

@app.route('/login_lost')
def login_lost() :
    abort(401); # Funcion que aborta la operacion (esta es similar a un break)

# Funcion que cunado la pagina tenga el errror 404 realice el codigo
@app.errorhandler(404)
def page_not_faund(error) :
     return 'Pagina no encontrada...', 404;

# Funcion que redirecciona a otra pagina
@app.route('/redirect')
def redirecion() :
     return redirect('/login_lost')
# Funcion que muestra una imagen guardada en el server(en mi caso en un directorio)
@app.route('/img')
def imagen() :
     return '<img src="' + url_for('static', filename='img/tux.png') + '"/>'

# Uso de template
@app.route('/hola')
@app.route('/hola/<nombre>')
def saluda(nombre = None) :
     return render_template('template1.html', nombre = nombre)

@app.route('/suma/<num1>/<num2>')
def suma(num1, num2) :
    try:
        resultado = int(num1) + int(num2)
    except :
        abort(404)
    return render_template('template2.html', num1  = num1, num2 = num2, resultado = resultado)

@app.route('/tabla/<numero>')
def tabla(numero) :
    try :
        num = int(numero)
    except :
        abort(404)
    return render_template('template3.html',numplantilla = num)

@app.route('/inicio')
def inicio() :
    # return render_template('formulario/inicio.html')
    lista = []
    for file in listdir(app.root_path + '/static/img') :
        lista.append(file)
    return render_template('form_subir_archivo/inicio2.html', lista = lista)

@app.route('/upload', methods=['get', 'post'])
def upload() :
    form = uploadForm()
    if form.validate_on_submit() :
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path + '/static/img/' + filename)
        return redirect(url_for('inicio'))
    return render_template('form_subir_archivo/upload.html', form = form)

@app.route('/calculadora_post', methods=['get', 'post'])
def calculadora_post():
    if request.method=='POST' :
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        operador = request.form.get('operador')

        try :
            resultado = eval(num1 + operador + num2)
        except:
            return render_template('formulario/error.html', error = 'No es posible realizar la operacion')

        return render_template('formulario/resultado.html', num1 = num1, num2 = num2, operador = operador, resultado = resultado)
    else :
        return render_template('formulario/calculadora_post.html')
    
@app.route('/calculadora_post_wtf', methods=['get', 'post'])
def calculadora_post_wtf() :
    form = formCalculadora(request.form)
    if form.validate_on_submit() :
        num1 = form.num1.data
        num2 = form.num2.data
        operador = form.operador.data
        try :
            resultado = eval(str(num1) + operador + str(num2))
        except :
            return render_template('formulario/error.html', error = 'No es posible realizar la operacion')
        
        return render_template('formulario/resultado.html', num1 = num1, num2 = num2, operador = operador, resultado = resultado)
    else :
        return render_template('formulario/calculadora_post_wtf.html', form = form)
    
