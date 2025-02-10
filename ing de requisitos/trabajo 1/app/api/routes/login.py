from flask import Blueprint, request, jsonify
from app.api.models.usuario import Usuario
from app.extensions import db

login_bp = Blueprint('login_bp', __name__, url_prefix='/login')

# Login
@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Faltan datos'}), 400
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    if usuario.password != data.get('password'):
        return jsonify({'error': 'Contraseña incorrecta'}), 401

    return jsonify({
        "message": "Login exitoso",
        "token": usuario.id
    })

# Logout
@login_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Sesión cerrada'})