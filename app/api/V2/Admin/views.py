from flask import Blueprint, request, jsonify

from app.api.V2.Auth.helper import token_require

from .models import Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v2')


@admin_bp.route('/menu', methods=['GET', 'POST'])
@token_require
def get_menu(current_user):
    if request.method == 'POST':
        if not current_user[1]:
            return jsonify({"Failed": "You are not an administrator"})
        data = request.get_json()
        meal_name = data.get('meal_name')
        meal_desc = data.get('meal_desc')
        meal_price = data.get('meal_price')
        return Admin().add_to_menu(meal_name, meal_desc, meal_price)

    return Admin().get_the_menu()

  
@admin_bp.route('/orders/', methods=['GET'])
@token_require
def view_orders(current_user):
    if not current_user[1]:
        return jsonify({"Failed": "You are not an administrator"})
    return Admin().all_orders()


@admin_bp.route('/orders/<order_id>', methods=['GET'])
@token_require
def view_specific_order(current_user, order_id):
    if not current_user[1]:
        return jsonify({"Failed": "You are not an administrator"})
    return Admin().get_user_orders(order_id)
