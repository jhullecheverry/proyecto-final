"""Modelos de datos del sistema"""
from backend.models.category import Category, db
from backend.models.product import Product

__all__ = ['Category', 'Product', 'db']