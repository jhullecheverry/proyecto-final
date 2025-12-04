import pytest
from backend.app import create_app
from backend.models.category import db
from backend.services.category_service import CategoryService
from backend.services.product_service import ProductService


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


class TestProductService:
    """Pruebas unitarias para ProductService"""

    def test_create_product_success(self, app):
        """Prueba crear un producto exitosamente"""
        with app.app_context():
            # Crear categoría primero
            category = CategoryService.create_category("Electrónica")

            # Crear producto
            product = ProductService.create_product(
                name="Laptop",
                price=1500.00,
                stock=10,
                category_id=category.id,
                description="Laptop de alta gama"
            )
            assert product.id is not None
            assert product.name == "Laptop"
            assert product.price == 1500.00
            assert product.stock == 10

    def test_create_product_empty_name(self, app):
        """Prueba crear producto con nombre vacío"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            with pytest.raises(ValueError, match="nombre del producto es requerido"):
                ProductService.create_product("", 100, 10, category.id)

    def test_create_product_negative_price(self, app):
        """Prueba crear producto con precio negativo"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            with pytest.raises(ValueError, match="precio debe ser un valor positivo"):
                ProductService.create_product("Laptop", -100, 10, category.id)

    def test_create_product_negative_stock(self, app):
        """Prueba crear producto con stock negativo"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            with pytest.raises(ValueError, match="stock debe ser un valor positivo"):
                ProductService.create_product("Laptop", 100, -5, category.id)

    def test_create_product_invalid_category(self, app):
        """Prueba crear producto con categoría inválida"""
        with app.app_context():
            with pytest.raises(ValueError, match="Categoría no encontrada"):
                ProductService.create_product("Laptop", 100, 10, 999)

    def test_get_all_products(self, app):
        """Prueba obtener todos los productos"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            ProductService.create_product("Laptop", 1500, 10, category.id)
            ProductService.create_product("Mouse", 25, 50, category.id)
            products = ProductService.get_all_products()
            assert len(products) == 2

    def test_get_product_by_id_success(self, app):
        """Prueba obtener producto por ID exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            created = ProductService.create_product("Laptop", 1500, 10, category.id)
            found = ProductService.get_product_by_id(created.id)
            assert found.name == "Laptop"

    def test_get_product_by_id_not_found(self, app):
        """Prueba obtener producto inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match="Producto no encontrado"):
                ProductService.get_product_by_id(999)

    def test_get_products_by_category(self, app):
        """Prueba obtener productos por categoría"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            ProductService.create_product("Laptop", 1500, 10, category.id)
            ProductService.create_product("Mouse", 25, 50, category.id)
            products = ProductService.get_products_by_category(category.id)
            assert len(products) == 2

    def test_update_product_success(self, app):
        """Prueba actualizar producto exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            product = ProductService.create_product("Laptop", 1500, 10, category.id)
            updated = ProductService.update_product(
                product.id,
                name="Laptop Gaming",
                price=2000,
                stock=5
            )
            assert updated.name == "Laptop Gaming"
            assert updated.price == 2000
            assert updated.stock == 5

    def test_delete_product_success(self, app):
        """Prueba eliminar producto exitosamente"""
        with app.app_context():
            category = CategoryService.create_category("Electrónica")
            product = ProductService.create_product("Laptop", 1500, 10, category.id)
            result = ProductService.delete_product(product.id)
            assert result is True
            with pytest.raises(ValueError):
                ProductService.get_product_by_id(product.id)