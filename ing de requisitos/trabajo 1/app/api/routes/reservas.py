from flask import Blueprint, request, jsonify
from app.models.reserva import Reserva
from app.extensions import db

reservas_bp = Blueprint('reservas_bp', __name__, url_prefix='/reservas')

# Obtener todas las reservas
@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    return jsonify([
        {
            "id": reserva.id,
            "fecha_inicio": reserva.fecha_inicio.isoformat(),
            "fecha_fin": reserva.fecha_fin.isoformat(),
            "usuario_id": reserva.usuario_id,
            "habitacion_id": reserva.habitacion_id
        } for reserva in reservas
    ])

# Obtener una reserva por ID
@reservas_bp.route('/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    return jsonify({
        "id": reserva.id,
        "fecha_inicio": reserva.fecha_inicio.isoformat(),
        "fecha_fin": reserva.fecha_fin.isoformat(),
        "usuario_id": reserva.usuario_id,
        "habitacion_id": reserva.habitacion_id
    })

# Crear una nueva reserva
@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Faltan datos'}), 400
    if not data.get('fecha_inicio') or not data.get('fecha_fin') or not data.get('usuario_id') or not data.get('habitacion_id'):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    nueva_reserva = Reserva(
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        usuario_id=data.get('usuario_id'),
        habitacion_id=data.get('habitacion_id')
    )

    db.session.add(nueva_reserva)
    db.session.commit()
    return jsonify({
        "message": "Reserva creada",
        "reserva": {
            "id": nueva_reserva.id,
            "fecha_inicio": nueva_reserva.fecha_inicio.isoformat(),
            "fecha_fin": nueva_reserva.fecha_fin.isoformat(),
            "usuario_id": nueva_reserva.usuario_id,
            "habitacion_id": nueva_reserva.habitacion_id
        }
    }), 201

# Actualizar una reserva
@reservas_bp.route('/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Faltan datos'}), 400
    if not data.get('fecha_inicio') or not data.get('fecha_fin') or not data.get('usuario_id') or not data.get('habitacion_id'):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    reserva.fecha_inicio = data.get('fecha_inicio')
    reserva.fecha_fin = data.get('fecha_fin')
    reserva.usuario_id = data.get('usuario_id')
    reserva.habitacion_id = data.get('habitacion_id')

    db.session.commit()
    return jsonify({
        "message": "Reserva actualizada",
        "reserva": {
            "id": reserva.id,
            "fecha_inicio": reserva.fecha_inicio.isoformat(),
            "fecha_fin": reserva.fecha_fin.isoformat(),
            "usuario_id": reserva.usuario_id,
            "habitacion_id": reserva.habitacion_id
        }
    })

# Eliminar una reserva
@reservas_bp.route('/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva eliminada'})
