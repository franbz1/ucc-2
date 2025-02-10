from flask import Blueprint, request, jsonify
from app.api.models.usuario import Usuario
from app.extensions import db

usuarios_bp = Blueprint('usuarios_bp', __name__, url_prefix='/usuarios')

# Dar todos los usuarios
@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
  usuarios = Usuario.query.all()
  return jsonify([{
      "id": usuario.id,
      "nombre": usuario.nombre,
      "email": usuario.email,
      "rol": usuario.rol
    } for usuario in usuarios])

# Dar un usuario por id
@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
  usuario = Usuario.query.get(id)
  if not usuario:
    return jsonify({'error': 'Usuario no encontrado'}), 404
  return jsonify({
    "id": usuario.id,
    "nombre": usuario.nombre,
    "email": usuario.email,
    "rol": usuario.rol
  })

# Crear un usuario
@usuarios_bp.route('/', methods=['POST'])
def create_usuario():
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Falta datos'}), 400
  if not data.get('nombre') or not data.get('email') or not data.get('password') or not data.get('rol'):
    return jsonify({'error': 'Faltan datos obligatorios'}), 400

  nuevo_usuario = Usuario(
    nombre=data.get('nombre'),
    email=data.get('email'),
    password=data.get('password'),
    rol=data.get('rol')
  )

  db.session.add(nuevo_usuario)
  db.session.commit()
  return jsonify({
    "message": "Usuario creado",
    "usuario": {
      "id": nuevo_usuario.id,
      "nombre": nuevo_usuario.nombre,
      "email": nuevo_usuario.email,
      "password": nuevo_usuario.password,
      "rol": nuevo_usuario.rol
    }
  })

# Actualizar un usuario
@usuarios_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Falta datos'}), 400
  if not data.get('nombre') or not data.get('email') or not data.get('password') or not data.get('rol'):
    return jsonify({'error': 'Faltan datos obligatorios'}), 400

  usuario = Usuario.query.get(id)
  if not usuario:
    return jsonify({'error': 'Usuario no encontrado'}), 404

  usuario.nombre = data.get('nombre')
  usuario.email = data.get('email')
  usuario.password = data.get('password')
  usuario.rol = data.get('rol')

  db.session.commit()
  return jsonify({
    "message": "Usuario actualizado",
    "usuario": {
      "id": usuario.id,
      "nombre": usuario.nombre,
      "email": usuario.email,
      "rol": usuario.rol
    }
  })

# Eliminar un usuario
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
  usuario = Usuario.query.get(id)
  if not usuario:
    return jsonify({'error': 'Usuario no encontrado'}), 404

  db.session.delete(usuario)
  db.session.commit()
  return jsonify({'message': 'Usuario eliminado'})