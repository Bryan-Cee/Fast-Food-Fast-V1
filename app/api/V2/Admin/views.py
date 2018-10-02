from flask import Blueprint, request

from .models import Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v2')


@admin_bp.route('/menu', methods=['GET', 'POST'])
def get_menu():
    if request.method == 'POST':
        data = request.get_json()
        meal_name = data.get('meal_name')
        meal_desc = data.get('meal_desc')
        meal_price = data.get('meal_price')
        return Admin().add_to_menu(meal_name, meal_desc, meal_price)

    return Admin().get_the_menu()

