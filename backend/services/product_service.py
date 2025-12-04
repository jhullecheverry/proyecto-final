from backend.models.product import Product
from backend.models.category import db
from backend.services.category_service import CategoryService


class ProductService:
    """Servicio para gestionar productos"""

    @staticmethod
    def create_product(name, price, stock, category_id, description=None):
        """Crea un nuevo producto"""
        # Validar nombre
        if not name or str(name).strip() == '':
            raise ValueError("El nombre del producto es requerido")

        # Validar precio
        if price is None:
            raise ValueError("El precio debe ser un valor positivo")

        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un valor numérico")

        if price < 0:
            raise ValueError("El precio debe ser un valor positivo")

        # Validar stock
        if stock is None:
            raise ValueError("El stock debe ser un valor positivo")

        try:
            stock = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un valor numérico")

        if stock < 0:
            raise ValueError("El stock debe ser un valor positivo")

        # Validar que la categoría existe
        CategoryService.get_category_by_id(category_id)

        product = Product(
            name=str(name).strip(),
            price=float(price),
            stock=int(stock),
            category_id=category_id,
            description=str(description).strip() if description else None
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_all_products():
        """Obtiene todos los productos"""
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        """Obtiene un producto por su ID"""
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        return product

    @staticmethod
    def get_products_by_category(category_id):
        """Obtiene productos de una categoría específica"""
        CategoryService.get_category_by_id(category_id)
        return Product.query.filter_by(category_id=category_id).all()

    @staticmethod
    def update_product(product_id, name=None, price=None, stock=None,
                       category_id=None, description=None):
        """Actualiza un producto"""
        product = ProductService.get_product_by_id(product_id)

        if name is not None:
            if str(name).strip() == '':
                raise ValueError("El nombre del producto no puede estar vacío")
            product.name = str(name).strip()

        if price is not None:
            try:
                price = float(price)
            except (TypeError, ValueError):
                raise ValueError("El precio debe ser un valor numérico")

            if price < 0:
                raise ValueError("El precio debe ser un valor positivo")
            product.price = float(price)

        if stock is not None:
            try:
                stock = int(stock)
            except (TypeError, ValueError):
                raise ValueError("El stock debe ser un valor numérico")

            if stock < 0:
                raise ValueError("El stock debe ser un valor positivo")
            product.stock = int(stock)

        if category_id is not None:
            CategoryService.get_category_by_id(category_id)
            product.category_id = category_id

        if description is not None:
            product.description = str(description).strip() if description else None

        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        """Elimina un producto"""
        product = ProductService.get_product_by_id(product_id)
        db.session.delete(product)
        db.session.commit()
        return True