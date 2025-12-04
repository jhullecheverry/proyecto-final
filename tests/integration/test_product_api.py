import pytest
import json
from backend.app import create_app
from backend.models.category import db


@pytest.fixture
def app():
    """Crea una aplicación de prueba"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()


@pytest.fixture
def category(client):
    """Crea una categoría de prueba"""
    response = client.post(
        '/api/categories',
        data=json.dumps({'name': 'Electrónica'}),
        content_type='application/json'
    )
    return json.loads(response.data)


class TestProductAPI:
    """Pruebas de integración para la API de productos"""

    def test_create_product_api(self, client, category):
        """Prueba crear producto vía API"""
        product_data = {
            'name': 'Laptop HP',
            'description': 'Laptop de alta gama',
            'price': 1500.00,
            'stock': 10,
            'category_id': category['id']
        }
        response = client.post(
            '/api/products',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Laptop HP'
        assert data['price'] == 1500.00
        assert 'id' in data

    def test_create_product_without_required_fields(self, client):
        """Prueba crear producto sin campos requeridos"""
        response = client.post(
            '/api/products',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_get_all_products_api(self, client, category):
        """Prueba obtener todos los productos vía API"""
        client.post('/api/products',
                   data=json.dumps({
                       'name': 'Laptop',
                       'price': 1500,
                       'stock': 10,
                       'category_id': category['id']
                   }),
                   content_type='application/json')

        client.post('/api/products',
                   data=json.dumps({
                       'name': 'Mouse',
                       'price': 25,
                       'stock': 50,
                       'category_id': category['id']
                   }),
                   content_type='application/json')

        response = client.get('/api/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2

    def test_get_product_by_id_api(self, client, category):
        """Prueba obtener producto por ID vía API"""
        create_response = client.post(
            '/api/products',
            data=json.dumps({
                'name': 'Laptop',
                'price': 1500,
                'stock': 10,
                'category_id': category['id']
            }),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['id']

        response = client.get(f'/api/products/{product_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Laptop'

    def test_get_products_by_category_api(self, client, category):
        """Prueba obtener productos por categoría vía API"""
        client.post('/api/products',
                   data=json.dumps({
                       'name': 'Laptop',
                       'price': 1500,
                       'stock': 10,
                       'category_id': category['id']
                   }),
                   content_type='application/json')

        response = client.get(f'/api/products?category_id={category["id"]}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1

    def test_update_product_api(self, client, category):
        """Prueba actualizar producto vía API"""
        create_response = client.post(
            '/api/products',
            data=json.dumps({
                'name': 'Laptop',
                'price': 1500,
                'stock': 10,
                'category_id': category['id']
            }),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['id']

        response = client.put(
            f'/api/products/{product_id}',
            data=json.dumps({
                'name': 'Laptop Gaming',
                'price': 2000
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Laptop Gaming'
        assert data['price'] == 2000

    def test_delete_product_api(self, client, category):
        """Prueba eliminar producto vía API"""
        create_response = client.post(
            '/api/products',
            data=json.dumps({
                'name': 'Laptop',
                'price': 1500,
                'stock': 10,
                'category_id': category['id']
            }),
            content_type='application/json'
        )
        product_id = json.loads(create_response.data)['id']

        response = client.delete(f'/api/products/{product_id}')
        assert response.status_code == 200

        get_response = client.get(f'/api/products/{product_id}')
        assert get_response.status_code == 404