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


class TestCategoryAPI:
    """Pruebas de integración para la API de categorías"""

    def test_create_category_api(self, client):
        """Prueba crear categoría vía API"""
        response = client.post(
            '/api/categories',
            data=json.dumps({'name': 'Electrónica'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Electrónica'
        assert 'id' in data

    def test_create_category_without_name(self, client):
        """Prueba crear categoría sin nombre"""
        response = client.post(
            '/api/categories',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_get_all_categories_api(self, client):
        """Prueba obtener todas las categorías vía API"""
        client.post('/api/categories',
                   data=json.dumps({'name': 'Electrónica'}),
                   content_type='application/json')
        client.post('/api/categories',
                   data=json.dumps({'name': 'Ropa'}),
                   content_type='application/json')

        response = client.get('/api/categories')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2

    def test_get_category_by_id_api(self, client):
        """Prueba obtener categoría por ID vía API"""
        create_response = client.post(
            '/api/categories',
            data=json.dumps({'name': 'Electrónica'}),
            content_type='application/json'
        )
        category_id = json.loads(create_response.data)['id']

        response = client.get(f'/api/categories/{category_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Electrónica'

    def test_get_category_not_found_api(self, client):
        """Prueba obtener categoría inexistente vía API"""
        response = client.get('/api/categories/999')
        assert response.status_code == 404

    def test_update_category_api(self, client):
        """Prueba actualizar categoría vía API"""
        create_response = client.post(
            '/api/categories',
            data=json.dumps({'name': 'Electrónica'}),
            content_type='application/json'
        )
        category_id = json.loads(create_response.data)['id']

        response = client.put(
            f'/api/categories/{category_id}',
            data=json.dumps({'name': 'Tecnología'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Tecnología'

    def test_delete_category_api(self, client):
        """Prueba eliminar categoría vía API"""
        create_response = client.post(
            '/api/categories',
            data=json.dumps({'name': 'Electrónica'}),
            content_type='application/json'
        )
        category_id = json.loads(create_response.data)['id']

        response = client.delete(f'/api/categories/{category_id}')
        assert response.status_code == 200

        get_response = client.get(f'/api/categories/{category_id}')
        assert get_response.status_code == 404

    def test_health_endpoint(self, client):
        """Prueba endpoint de health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'