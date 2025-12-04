from flask import Flask
from flask_cors import CORS
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config import config
from backend.models.category import db
from backend.models.product import Product
from backend.controllers.category_controller import category_bp
from backend.controllers.product_controller import product_bp


def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    CORS(app)

    db.init_app(app)

    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)

    @app.route('/')
    def index():
        return {
            'message': 'API de Gestión de Inventario',
            'version': '1.0',
            'endpoints': {
                'categories': '/api/categories',
                'products': '/api/products'
            }
        }

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000, debug=True)