from flask import session

def login_user(Usuario) :
    session['id'] = Usuario.id
    session['username'] = Usuario.username
    session['admin'] = Usuario.admin

def logout_user() :
    session.pop('id', None)
    session.pop('username', None)
    session.pop('admin', None)

def is_login() :
    return session.get('id') is not None

def is_admin() :
    return session.get('admin') == True