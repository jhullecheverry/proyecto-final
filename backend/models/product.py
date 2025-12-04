from backend.models.category import db


class Product(db.Model):
    """Modelo de Producto"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
                            nullable=False)

    def __init__(self, name, price, stock, category_id, description=None):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id

    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

    def __repr__(self):
        return f'<Product {self.name}>'