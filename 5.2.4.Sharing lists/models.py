# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class DatabaseVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(10), nullable=False, default='1.0')

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)
    listas = db.relationship('Lista', backref='usuario', lazy=True)
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True)
    suscripciones = db.relationship('Suscripcion', backref='usuario', lazy=True)
    likes = db.relationship('Like', backref='usuario', lazy=True)
    checkeds = db.relationship('Checked', backref='usuario', lazy=True)

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))
    visibilidad = db.Column(db.String(20), nullable=False, default='publica')
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contador_favoritos = db.Column(db.Integer, default=0)
    items = db.relationship('Item', backref='lista', lazy=True)
    etiquetas = db.relationship('ListaEtiqueta', backref='lista', lazy=True)
    likes = db.relationship('Like', backref='lista_ref', lazy=True)  # Cambiado 'lista_likes' a 'lista_ref'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    enlace = db.Column(db.String(200))
    imagen = db.Column(db.String(200))
    orden = db.Column(db.Integer)
    etiquetas = db.relationship('ItemEtiqueta', backref='item', lazy=True)
    likes = db.relationship('Like', backref='item_ref', lazy=True)  # Cambiado 'item_likes' a 'item_ref'
    checkeds = db.relationship('Checked', backref='item_checkeds', lazy=True)

class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class ListaEtiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('etiqueta.id'), nullable=False)
    etiqueta = db.relationship('Etiqueta', backref='listas_etiquetas')

class ItemEtiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('etiqueta.id'), nullable=False)
    etiqueta = db.relationship('Etiqueta', backref='items_etiquetas')

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)

class Suscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'))
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'))
    lista = db.relationship('Lista', backref='likes_ref', lazy=True)  # Cambiado 'likes_lista' a 'likes_ref'
    item = db.relationship('Item', backref='likes_item_ref', lazy=True)  # Cambiado 'likes_item' a 'likes_item_ref'

class Checked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    fecha_checked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)