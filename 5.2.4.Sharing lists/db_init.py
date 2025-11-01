# db_init.py
from models import db, DatabaseVersion, Usuario, Lista, Item, Etiqueta, ListaEtiqueta, Checked
from app import create_app
import bcrypt

app = create_app()
with app.app_context():
    db.create_all()
    db_version = DatabaseVersion(version='1.0')
    db.session.add(db_version)
    hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin_user = Usuario(nombre_usuario='admin', email='admin@example.com', contrasena=hashed_password)
    db.session.add(admin_user)
    db.session.commit()
    lista1 = Lista(id_usuario=1, titulo='Lista Pública', descripcion='Una lista pública', visibilidad='publica')
    lista2 = Lista(id_usuario=1, titulo='Lista Privada', descripcion='Una lista privada', visibilidad='privada')
    db.session.add_all([lista1, lista2])
    db.session.commit()
    etiqueta1 = Etiqueta(nombre='prueba')
    etiqueta2 = Etiqueta(nombre='personal')
    db.session.add_all([etiqueta1, etiqueta2])
    db.session.commit()
    lista_etiqueta1 = ListaEtiqueta(id_lista=1, id_etiqueta=1)
    lista_etiqueta2 = ListaEtiqueta(id_lista=2, id_etiqueta=2)
    db.session.add_all([lista_etiqueta1, lista_etiqueta2])
    db.session.commit()