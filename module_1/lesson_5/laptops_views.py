from flask import render_template, Blueprint, request
from app_config import laptops

laptops_app = Blueprint('laptops_app', __name__)


def get_laptop_info(laptop_id):
    for laptop in laptops:
        if laptop_id == laptop['id']:
            return laptop


@laptops_app.route('/', endpoint='laptops')
def products_page():
    return '<h1>Laptops Page!</h1>'


@laptops_app.route('/<int:laptop_id>/', endpoint='laptop')
def product_page(laptop_id):
    laptop = get_laptop_info(laptop_id)
    response = render_template(
        'laptop_info.html',
        laptop=laptop,
    )
    return response
