import os
from flask import Flask, abort, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap5
from aplication import config
from aplication.form import formArticulos, formCategorias
from werkzeug.utils import secure_filename
from aplication.model import Articulos, Categorias, db


app = Flask(__name__)
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
    art = Articulos.query.get(id) # Optengo el id por parametro de a ruta

    if art is None :
        abort(404)

    form = formArticulos(obj = art) # Cargo el formulario con los datos necesarios
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias

    if form.validate_on_submit() :
        if form.photo.data : # En caso de subir una nueva imagen elimino la anterior

            if art.image : os.remove(app.root_path + '/static/img/' + art.image) # Si tiene imagen asociada la elimino

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