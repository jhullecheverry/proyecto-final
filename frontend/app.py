from flask import Flask, render_template
import os

app = Flask(__name__)

API_URL = os.getenv('API_URL', 'http://localhost:5000')


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', api_url=API_URL)


@app.route('/categories')
def categories():
    """Página de gestión de categorías"""
    return render_template('categories.html', api_url=API_URL)


@app.route('/products')
def products():
    """Página de gestión de productos"""
    return render_template('products.html', api_url=API_URL)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)