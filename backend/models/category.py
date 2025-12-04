from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    """Modelo de Categoría"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relación con productos
    products = db.relationship('Product', backref='category', lazy=True,
                               cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'product_count': len(self.products)
        }

    def __repr__(self):
        return f'<Category {self.name}>'