import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

###Ejemplo
# post_tags = Table('post_tags', Base.metadata,
#     Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
#     Column('page_id', Integer, ForeignKey('pages.id'), primary_key=True)
# )

# class Page(Base):
#     __tablename__ = 'pages'

#     id = Column(Integer, primary_key=True)
#     tags = relationship('Tag', secondary=post_tags, lazy='subquery',backref=backref('pages', lazy=True))

# class Tag(Base):
#     __tablename__ = 'tag'
#     id = Column(Integer, primary_key=True)


# Tabla con cardinalidad N-N (muchos a muchos) se tiene que hacer con esta sintaxis
posts_guardados = Table('posts_guardados', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('usuarios.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

# Tabla con cardinalidad N-N (muchos a muchos) se tiene que hacer con esta sintaxis
seguidores_seguidos = Table('seguidores_seguidos', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('seguido_id', Integer, ForeignKey('usuarios.id')),
    Column('seguidor_id', Integer, ForeignKey('usuarios.id'))
)

# Tabla con cardinalidad N-N (muchos a muchos) se tiene que hacer con esta sintaxis
comentarios_posts = Table('comentarios_posts', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('fecha', Date, nullable=False),
    Column('hora', DateTime, nullable=False),
    Column('comentario', String(250), nullable=False),
    Column('user_id', Integer, ForeignKey('usuarios.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    post_id = relationship('Post', backref='usuarios', lazy=True) #Relacion 1:N con Post(Un usuario puede tener muchos posts)
    historia_id = relationship('Historia', backref='usuarios', lazy=True) #Relacion 1:N con Historia(Un usuario puede tener muchas historias)
    chat_seguidores_rec_id = relationship('ChatSeguidores', backref='usuarios', lazy=True) #Relacion 1:N con ChatSeguidores(Un usuario puede tener muchos chats)
    chat_seguidores_emi_id = relationship('ChatSeguidores', backref='usuarios', lazy=True) #Relacion 1:N con ChatSeguidores(Un usuario puede tener muchos chats)
    posts_guardados = relationship('Usuario', secondary=seguidores_seguidos, lazy='subquery',backref=backref('usuarios', lazy=True)) #Relaciona tabla usuario y seguidores_seguidos
    comentarios_posts = relationship('Usuario', secondary=comentarios_posts, lazy='subquery',backref=backref('usuarios', lazy=True)) #Relaciona tabla usuario y comentarios_posts

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(250), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(DateTime, nullable=False)
    contenido = Column(String(250), nullable=False)
    multimedia = Column(String(250), nullable=False)
    etiquetas = Column(String(250), nullable=False)
    hashtag = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('usuarios.id')) #Relacion N:1 con Usuario(El post es de un usuario)
    posts_guardados = relationship('Usuario', secondary=posts_guardados, lazy='subquery',backref=backref('posts', lazy=True)) #Relaciona tabla usuario y post

class Historia(Base):
    __tablename__ = 'historias'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(250), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(DateTime, nullable=False)
    contenido = Column(String(250), nullable=False)
    multimedia = Column(String(250), nullable=False)
    etiquetas = Column(String(250), nullable=False)
    hashtag = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False) #Relacion N:1 con Usuario(La historia es de un usuario)

class ChatSeguidores(Base):
    __tablename__ = 'chat_seguidores'

    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    hora = Column(DateTime, nullable=False)
    mensaje = Column(String(250), nullable=False)
    multimedia = Column(String(250), nullable=False)
    receptor_id = Column(Integer, ForeignKey('usuarios.id') , nullable=False)
    emisor_id = Column(Integer, ForeignKey('usuarios.id') , nullable=False)



## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')