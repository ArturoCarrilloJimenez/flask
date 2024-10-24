from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

# Clases de categorias
class Categorias(db.Model) :
    """Categorías de los articulos"""
    __tablename__ = 'categorias'

    # Columnas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)

    # Relacion foreing Key
    articulos = relationship('Articulos', cascade='all, delete-orphan', backref='Categorias', lazy='dynamic')
    
    # Funciones
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self = self))
    
class Articulos(db.Model) : # Clases de articulos
    """Articulos de nuestra tienda"""
    __tablename__ = 'articulos'

    # Columnas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, default=0)
    iva = Column(Integer, default=21)
    descripcion = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer, default=0)
    
    # Relacion foreing Key
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categorias = relationship('Categorias', backref='Articulos')
    
    # Funciones
    def precio_final(self) :
        return self.precio+(self.precio*self.iva/100)
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self = self))

class Usuarios(db.Model, UserMixin) : # Clases de usuarios
    """Registro de Usuarios"""
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    admin = Column(Boolean, default=False)

    # Funciones
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self = self))
    
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    
    @password.setter
    def password(self, password) :
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) :
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self) :
        return self.admin
