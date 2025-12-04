from flask import Blueprint, request, jsonify
from backend.services.product_service import ProductService

product_bp = Blueprint('products', __name__, url_prefix='/api/products')


@product_bp.route('', methods=['GET'])
def get_products():
    """Obtiene todos los productos"""
    try:
        category_id = request.args.get('category_id', type=int)
        if category_id:
            products = ProductService.get_products_by_category(category_id)
        else:
            products = ProductService.get_all_products()
        return jsonify([prod.to_dict() for prod in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto por ID"""
    try:
        product = ProductService.get_product_by_id(product_id)
        return jsonify(product.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('', methods=['POST'])
def create_product():
    """Crea un nuevo producto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        product = ProductService.create_product(
            name=data.get('name'),
            price=data.get('price'),
            stock=data.get('stock'),
            category_id=data.get('category_id'),
            description=data.get('description')
        )
        return jsonify(product.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        product = ProductService.update_product(
            product_id=product_id,
            name=data.get('name'),
            price=data.get('price'),
            stock=data.get('stock'),
            category_id=data.get('category_id'),
            description=data.get('description')
        )
        return jsonify(product.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto"""
    try:
        ProductService.delete_product(product_id)
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500