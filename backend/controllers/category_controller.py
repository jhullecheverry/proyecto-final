from flask import Blueprint, request, jsonify
from backend.services.category_service import CategoryService

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@category_bp.route('', methods=['GET'])
def get_categories():
    """Obtiene todas las categorías"""
    try:
        categories = CategoryService.get_all_categories()
        return jsonify([cat.to_dict() for cat in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Obtiene una categoría por ID"""
    try:
        category = CategoryService.get_category_by_id(category_id)
        return jsonify(category.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('', methods=['POST'])
def create_category():
    """Crea una nueva categoría"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        name = data.get('name')
        category = CategoryService.create_category(name)
        return jsonify(category.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Actualiza una categoría"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        name = data.get('name')
        category = CategoryService.update_category(category_id, name)
        return jsonify(category.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Elimina una categoría"""
    try:
        CategoryService.delete_category(category_id)
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500