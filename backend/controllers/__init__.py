"""Controladores de la API REST"""
from backend.controllers.category_controller import category_bp
from backend.controllers.product_controller import product_bp

__all__ = ['category_bp', 'product_bp']