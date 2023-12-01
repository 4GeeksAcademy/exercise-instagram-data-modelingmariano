from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    contraseña = Column(String(100), nullable=False)
    bio = Column(String(500))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    publicaciones = relationship('Publicacion', back_populates='usuario')
    comentarios = relationship('Comentario', back_populates='usuario')
    seguidores = relationship('Seguir', foreign_keys='Seguir.seguido_id', back_populates='seguido')
    siguiendo = relationship('Seguir', foreign_keys='Seguir.seguidor_id', back_populates='seguidor')

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    imagen_url = Column(String(255), nullable=False)
    descripcion = Column(String(500))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    

    usuario = relationship('Usuario', back_populates='publicaciones')
    comentarios = relationship('Comentario', back_populates='publicacion')

class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    texto = Column(String(500), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='comentarios')
    publicacion = relationship('Publicacion', back_populates='comentarios')

class Seguir(Base):
    __tablename__ = 'seguir'
    id = Column(Integer, primary_key=True)
    seguidor_id = Column(Integer, ForeignKey('usuario.id'))
    seguido_id = Column(Integer, ForeignKey('usuario.id'))

    seguidor = relationship('Usuario', foreign_keys=[seguidor_id], back_populates='siguiendo')
    seguido = relationship('Usuario', foreign_keys=[seguido_id], back_populates='seguidores')

# Generar el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e
