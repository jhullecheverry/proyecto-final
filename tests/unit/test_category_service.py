import pytest
from backend.app import create_app
from backend.models.category import db, Category
from backend.services.category_service import CategoryService


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


class TestCategoryService:
    """Pruebas unitarias para CategoryService"""

    def test_create_category_success(self, app):
        """Prueba crear una categoría exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            assert category.id is not None
            assert category.name == "Electrónica"

    def test_create_category_empty_name(self, app):
        """Prueba crear categoría con nombre vacío"""
        with app.app_context():
            with pytest.raises(ValueError, match="nombre de la categoría es requerido"):
                CategoryService.create_category("")

    def test_create_category_duplicate(self, app):
        """Prueba crear categoría duplicada"""
        with app.app_context():
            CategoryService.create_category("Electrónica")
            with pytest.raises(ValueError, match="Ya existe una categoría"):
                CategoryService.create_category("Electrónica")

    def test_get_all_categories(self, app):
        """Prueba obtener todas las categorías"""
        with app.app_context():
            CategoryService.create_category("Electrónica")
            CategoryService.create_category("Ropa")
            categories = CategoryService.get_all_categories()
            assert len(categories) == 2

    def test_get_category_by_id_success(self, app):
        """Prueba obtener categoría por ID exitosamente"""
        with app.app_context():
            created = CategoryService.create_category("Electrónica")
            found = CategoryService.get_category_by_id(created.id)
            assert found.name == "Electrónica"

    def test_get_category_by_id_not_found(self, app):
        """Prueba obtener categoría inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match="Categoría no encontrada"):
                CategoryService.get_category_by_id(999)

    def test_update_category_success(self, app):
        """Prueba actualizar categoría exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            updated = CategoryService.update_category(category.id, "Tecnología")
            assert updated.name == "Tecnología"

    def test_update_category_duplicate_name(self, app):
        """Prueba actualizar con nombre duplicado"""
        with app.app_context():
            cat1 = CategoryService.create_category("Electrónica")
            cat2 = CategoryService.create_category("Ropa")
            with pytest.raises(ValueError, match="Ya existe otra categoría"):
                CategoryService.update_category(cat2.id, "Electrónica")

    def test_delete_category_success(self, app):
        """Prueba eliminar categoría exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            result = CategoryService.delete_category(category.id)
            assert result is True
            with pytest.raises(ValueError):
                CategoryService.get_category_by_id(category.id)