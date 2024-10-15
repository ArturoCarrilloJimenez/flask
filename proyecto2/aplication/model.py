from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Clases de categorias
class Categorias(db.Model) :
    """Categorías de los articulos"""
    __tablename__ = 'categorias'

    # Columnas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

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
    nombre = Column(String(100), nullable=False)
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
