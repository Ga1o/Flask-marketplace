from flask import Blueprint

product_bp = Blueprint('product_bp', __name__, template_folder='templates/product_bp')

from . import routes
