import os
from flask import Flask, abort, json, render_template, url_for, redirect, request, make_response
from flask_bootstrap import Bootstrap5
from application import config
from application.form import formArticulos, formCategorias, formChangePassword, formSiNo, formUser, LoginForm, formCarrrito
from werkzeug.utils import secure_filename
from application.model import Articulos, Categorias, Usuarios, db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# App
app = Flask(__name__)

# Charge login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id) :
    return Usuarios.query.get(int(user_id))

# Charge bootstrap
bootstrap = Bootstrap5(app)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
@app.route('/categoria/<id>')
def inicio(id='0') :
    categoria = Categorias.query.get(id)
    if id == '0' :
        articulos = Articulos.query.all()
    else :
        articulos = Articulos.query.filter_by(CategoriaId = id)
    categorias = Categorias.query.all()
    return render_template('inicio.html', articulos = articulos, categorias = categorias, categoria = categoria)

@app.route('/categorias')
def categorias() :
    categorias = Categorias.query.all()
    return render_template('categorias.html', categorias = categorias)

@app.errorhandler(404)
def page_not_found(error) :
    return render_template('error.html', error = 'Página no encontrada...'), 404

@app.route('/articulos/new', methods=['get', 'post'])
def articulos_new() :
    if not current_user.is_admin() :
        return redirect(url_for('inicio'))
    
    form = formArticulos()
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[0:]] # [0:] devuelve la lista sin filtros, 0 siendo el inicio y : el fin
    form.CategoriaId.choices = categorias
    if form.validate_on_submit() :
        try : # Guardado de imagen
            f = form.photo.data
            filename = secure_filename(f.filename)

            # Optiene la ruta completa de la imagen
            upload_folder = os.path.join(app.root_path, 'static/img/')
            file_path = os.path.join(upload_folder, filename)

            # Guarda la imagen en la ruta anterior
            f.save(file_path)
        except :
            filename = ''
        art = Articulos()
        form.populate_obj(art)
        art.image = filename
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('inicio'))
    else :
        return render_template('articulos_new.html', form = form)
    
@app.route('/categorias/new', methods=['get', 'post'])
def categorias_new() :
    if not current_user.is_admin() :
        return redirect(url_for('inicio'))
    
    form = formCategorias(request.form)
    if form.validate_on_submit() :
        cat = Categorias(nombre = form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('categorias'))
    else :
        return render_template('categorias_new.html',form = form)
    
@app.route('/articulos/<id>/edit', methods=['get', 'post'])
def articulos_edit(id) :
    if not current_user.is_admin() :
        return redirect(url_for('inicio'))
    
    art = Articulos.query.get(id) # Optengo el id por parametro de a ruta

    if art is None :
        abort(404)

    form = formArticulos(obj = art) # Cargo el formulario con los datos necesarios
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias

    if form.validate_on_submit() :
        if form.photo.data : # En caso de subir una nueva imagen elimino la anterior

            if art.image : 
                count_img = Articulos.query.filter_by(image=art.image).count() # Saco todos los registros con esa imagen
                if count_img == 1 : # Si solo hay uno, lo elimino
                    os.remove(app.root_path + '/static/img/' + art.image) # Si tiene imagen asociada la elimino

            try : # Guardado de imagen
                f = form.photo.data
                filename = secure_filename(f.filename)

                # Optiene la ruta completa de la imagen
                upload_folder = os.path.join(app.root_path, 'static/img/')
                file_path = os.path.join(upload_folder, filename)

                # Guarda la imagen en la ruta anterior
                f.save(file_path)
            except :
                filename = ''
        else :
            filename = art.image
        form.populate_obj(art)
        art.image = filename
        db.session.commit()
        return redirect(url_for('inicio'))

    return render_template('articulos_new.html', form=form)

@app.route('/articulos/<id>/delete', methods=['get', 'post'])
def articulos_delete(id) :
    if not current_user.is_admin() :
        return redirect(url_for('inicio'))
    
    art = Articulos.query.get(id) # Optengo el id por parametro de a ruta

    if art is None :
        abort(404)
    
    form = formSiNo()

    if form.validate_on_submit() :
        if form.si.data :
            if art.image :
                count_img = Articulos.query.filter_by(image=art.image).count() # Saco todos los registros con esa imagen y los cuenta

                if count_img == 1 : # Si solo hay uno, lo elimino
                    os.remove(app.root_path + '/static/img/' + art.image) # Si tiene imagen asociada la elimino

            db.session.delete(art)
            db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('articulos_delete.html', form = form, art = art)

@app.route('/categorias/<id>/edit', methods=['get', 'post'])
def categorias_edit(id) :
    if not current_user.is_admin() :
        return redirect(url_for('categorias'))
    
    cat = Categorias.query.get(id)

    if cat is None :
        abort(404)

    form = formCategorias(request.form, obj = cat)
    if form.validate_on_submit() :
        form.populate_obj(cat)
        db.session.commit()
        return redirect(url_for('categorias'))
    return render_template('categorias_new.html', form = form)

@app.route('/categorias/<id>/delete', methods=['get', 'post'])
def categorias_delete(id) :
    if not current_user.is_admin() :
        return redirect(url_for('categorias'))
    
    cat = Categorias.query.get(id)

    if cat is None :
        abort(404)

    form = formSiNo()
    if form.validate_on_submit() :
        if form.si.data :
            db.session.delete(cat)
            db.session.commit()
        return redirect(url_for('categorias'))
    return render_template('categorias_delete.html', form = form, cat = cat)

@app.route('/login', methods=['get', 'post'])
def login() :
    if current_user.is_authenticated :
        abort(404)
    
    form = LoginForm()
    if form.validate_on_submit() :
        user = Usuarios.query.filter_by(username = form.username.data).first()
        if user!=None and user.verify_password(form.password.data) :
            login_user(user)
            next  = request.args.get('next')
            return redirect(next or url_for('inicio'))
        form.username.errors.append('Usuario o contraseña incorrecta')
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout() :
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro', methods=['get', 'post'])
def registro():
    if current_user.is_authenticated :
        abort(404)
    
    form = formUser()
    if form.validate_on_submit() :
        existe_usuario = Usuarios.query.filter_by(username = form.username.data).first()
        if existe_usuario is None :
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        form.username.errors.append('Nombre de usuario ya existe')
    return render_template('registro.html', form = form)

@app.route('/perfil/<username>', methods=['get', 'post'])
@login_required
def perfil(username) :
    user = Usuarios().query.filter_by(username = username).first()
    if user is None :
        abort(404)
    form = formUser(request.form, obj = user)
    del form.password
    if form.validate_on_submit() :
        form.populate_Obj(user)
        db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('registro.html', form = form, perfil = True)

@app.route('/changepassword/<username>', methods=['get', 'post'])
@login_required
def changepassword(username) :
    user = Usuarios.query.filter_by(username = username).first()
    if user is None :
        abort(404)
    
    form = formChangePassword()
    if form.validate_on_submit() :
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('changepassword.html', form = form)

@app.route('/carrito/add/<id>', methods=['get', 'post'])
@login_required
def add_carrito(id) :
    art = Articulos.query.get(id)

    if art is None :
        abort(404)
    
    form = formCarrrito()
    form.id.data = id
    if form.validate_on_submit() :
        if art.stock >= int(form.cantidad.data) :
            try :
                datos = json.loads(request.cookies.get(str(current_user.id)))
            except :
                datos = []

            actualizar = False

            for data in datos :
                if data['id'] == id :
                    data['cantidad'] = form.cantidad.data
                    actualizar = True
            
            if not actualizar:
                datos.append({'id' : id, 'cantidad' : form.cantidad.data})
            resp = make_response(redirect(url_for('inicio')))
            resp.set_cookie(str(current_user.id), json.dumps(datos))
            return resp
        form.cantidad.errors.append('No hay articulos suficientes')
    return render_template('carrito_add.html', form = form, art = art)

@app.route('/carrito')
@login_required
def carrito() :
    try :
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except :
        datos = []
    articulos = []
    cantidad = []
    total = 0
    for data in datos :
        articulos.append(Articulos.query.get(data['id']))
        cantidad.append(data['cantidad'])
        total += Articulos.query.get(data['id']).precio_final() * data['cantidad']
    articulos = zip(articulos, cantidad)

    return render_template('carrito.html', articulos = articulos, total = total)

@app.context_processor
def contar_carrito() :
    if not current_user.is_authenticated :
        return {'num_articulos' : 0}
    if request.cookies.get(str(current_user.id)) is None :
        return {'num_articulos' : 0}
    else :
        datos = json.loads(request.cookies.get(str(current_user.id)))
        return {'num_articulos' : len(datos)}

@app.route('/carrito_delete/<id>')
@login_required
def carrito_delete(id) :
    try :
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except :
        datos = []
    new_datos = []
    for date in datos :
        if date['id'] != id :
            new_datos.append(date)
    resp = make_response(redirect(url_for('carrito')))
    resp.set_cookie(str(current_user.id), json.dumps(new_datos))
    return resp

@app.route('/pedido')
@login_required
def pedido() :
    try :
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except :
        datos = []
    total = 0
    for data in datos :
        total += Articulos.query.get(data['id']).precio_final() * data['cantidad']
        Articulos.query.get(data['id']).stock -= data['cantidad']
        db.session.commit()
    resp = make_response(render_template('pedido.html', total = total))
    resp.set_cookie(str(current_user.id), '', expires=0)
    return resp