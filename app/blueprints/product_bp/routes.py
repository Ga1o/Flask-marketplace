from flask import render_template
from . import product_bp


@product_bp.route('/add_product')
def add_product():
    return render_template('add_product.html')

