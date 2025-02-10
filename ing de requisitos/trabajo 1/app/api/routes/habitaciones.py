from flask import Blueprint, request, jsonify
from app.models.habitacion import Habitacion
from app.extensions import db

habitaciones_bp = Blueprint('habitaciones_bp', __name__, url_prefix='/habitaciones')

# Obtener todas las habitaciones
@habitaciones_bp.route('/', methods=['GET'])
def get_habitaciones():
    habitaciones = Habitacion.query.all()
    return jsonify([
        {
            "id": habitacion.id,
            "numero": habitacion.numero,
            "costo_por_noche": habitacion.costo_por_noche
        } for habitacion in habitaciones
    ])

# Obtener una habitación por ID
@habitaciones_bp.route('/<int:id>', methods=['GET'])
def get_habitacion(id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({'error': 'Habitación no encontrada'}), 404
    return jsonify({
        "id": habitacion.id,
        "numero": habitacion.numero,
        "costo_por_noche": habitacion.costo_por_noche
    })

# Crear una nueva habitación
@habitaciones_bp.route('/', methods=['POST'])
def create_habitacion():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Faltan datos'}), 400
    if not data.get('numero') or not data.get('costo_por_noche'):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    nueva_habitacion = Habitacion(
        numero=data.get('numero'),
        costo_por_noche=data.get('costo_por_noche')
    )

    db.session.add(nueva_habitacion)
    db.session.commit()
    return jsonify({
        "message": "Habitación creada",
        "habitacion": {
            "id": nueva_habitacion.id,
            "numero": nueva_habitacion.numero,
            "costo_por_noche": nueva_habitacion.costo_por_noche
        }
    }), 201

# Actualizar una habitación
@habitaciones_bp.route('/<int:id>', methods=['PUT'])
def update_habitacion(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Faltan datos'}), 400
    if not data.get('numero') or not data.get('costo_por_noche'):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({'error': 'Habitación no encontrada'}), 404

    habitacion.numero = data.get('numero')
    habitacion.costo_por_noche = data.get('costo_por_noche')

    db.session.commit()
    return jsonify({
        "message": "Habitación actualizada",
        "habitacion": {
            "id": habitacion.id,
            "numero": habitacion.numero,
            "costo_por_noche": habitacion.costo_por_noche
        }
    })

# Eliminar una habitación
@habitaciones_bp.route('/<int:id>', methods=['DELETE'])
def delete_habitacion(id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({'error': 'Habitación no encontrada'}), 404

    db.session.delete(habitacion)
    db.session.commit()
    return jsonify({'message': 'Habitación eliminada'})
