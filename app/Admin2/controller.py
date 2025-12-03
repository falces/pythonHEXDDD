"""
Controlador REST para Admin2.
Endpoints CRUD de usuarios.
"""
from flask import Blueprint, request, jsonify
from Admin2.services import UserService

admin2_bp = Blueprint('admin2', __name__, url_prefix='/api/v1/admin2')
user_service = UserService()


@admin2_bp.route('/users', methods=['POST'])
def create_user():
    """Crea un nuevo usuario."""
    data = request.get_json() or {}
    
    # Validación simple
    if not data.get('username'):
        return jsonify({'error': 'username is required'}), 400
    if not data.get('email'):
        return jsonify({'error': 'email is required'}), 400
    
    try:
        user = user_service.create(
            username=data['username'],
            email=data['email']
        )
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409


@admin2_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id: str):
    """Obtiene un usuario por ID."""
    user = user_service.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())


@admin2_bp.route('/users', methods=['GET'])
def get_all_users():
    """Obtiene todos los usuarios."""
    users = user_service.get_all()
    return jsonify([u.to_dict() for u in users])


@admin2_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id: str):
    """Actualiza un usuario."""
    data = request.get_json() or {}
    
    try:
        user = user_service.update(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email')
        )
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 409


@admin2_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Elimina un usuario."""
    deleted = user_service.delete(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return '', 204
