from flask import Blueprint, request, jsonify, make_response

from app.auth.helper import token_require

from .models import Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v2')


@admin_bp.route('/menu', methods=['GET', 'POST'])
@token_require
def get_menu(current_user):
    if request.method == 'POST':
        if not current_user['admin']:
            return jsonify({"status": "failed", "message": "You are not an administrator"}), 401
        data = request.get_json(force=True)
        meal_name = data.get('meal_name')
        meal_desc = data.get('meal_desc')
        if not meal_desc:
            meal_desc = 'Tasty and sweet'
        meal_price = data.get('meal_price')
        return Admin().add_to_menu(meal_name, meal_desc, meal_price)
    return Admin().get_the_menu()

  
@admin_bp.route('/orders/', methods=['GET'])
@token_require
def view_orders(current_user):
    if not current_user['admin']:
        return jsonify({"status": "failed", "message": "You are not an administrator"}), 401
    return Admin().all_orders()


@admin_bp.route('/orders/<order_id>', methods=['GET', 'PUT'])
@token_require
def view_specific_order(current_user, order_id):
    if request.method == 'PUT':
        if not current_user['admin']:
            return jsonify({"status": "Failed", "message": "You are not an administrator"}), 401
        data = request.get_json(force=True)
        status = data.get('status')
        if status not in ('processing', 'cancelled', 'complete'):
            prompt = ({'status':'failed', 'message':"Please enter the required status in the correct format: 'status':'the_status' which can be 'processing', 'complete' or 'cancelled'"})
            return make_response(jsonify(prompt), 400)
        return Admin().modify_order(order_id, status)
    if not current_user['admin']:
        return jsonify({"status": "Failed", "message": "You are not an administrator"}), 401
    return Admin().get_user_orders(order_id)


@admin_bp.route('/users/<user_id>', methods=['PUT'])
@token_require
def make_user_admin(current_user, user_id):
    if not current_user['admin']:
        return jsonify({"status": "Failed", "message": "You are not an administrator"}), 401
    data = request.get_json(force=True)
    admin = data.get('admin')
    return Admin().promote_user(admin, user_id)
