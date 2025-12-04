from backend.models.category import Category, db


class CategoryService:
    """Servicio para gestionar categorías"""

    @staticmethod
    def create_category(name):
        """Crea una nueva categoría"""
        if not name or name.strip() == '':
            raise ValueError("El nombre de la categoría es requerido")

        existing = Category.query.filter_by(name=name).first()
        if existing:
            raise ValueError("Ya existe una categoría con ese nombre")

        category = Category(name=name.strip())
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all_categories():
        """Obtiene todas las categorías"""
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        """Obtiene una categoría por su ID"""
        category = Category.query.get(category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        return category

    @staticmethod
    def update_category(category_id, name):
        """Actualiza una categoría"""
        category = CategoryService.get_category_by_id(category_id)

        if not name or name.strip() == '':
            raise ValueError("El nombre de la categoría es requerido")

        existing = Category.query.filter(
            Category.name == name,
            Category.id != category_id
        ).first()

        if existing:
            raise ValueError("Ya existe otra categoría con ese nombre")

        category.name = name.strip()
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id):
        """Elimina una categoría"""
        category = CategoryService.get_category_by_id(category_id)

        if len(category.products) > 0:
            raise ValueError(
                "No se puede eliminar una categoría con productos asociados"
            )

        db.session.delete(category)
        db.session.commit()
        return True