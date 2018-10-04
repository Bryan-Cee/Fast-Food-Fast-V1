from flask import Blueprint, request, make_response, redirect, jsonify
import datetime

from app.api.v2.auth.helper import token_require


user = Blueprint('users', __name__, url_prefix='/api/v2')


@user.route('/', methods=['GET'])
def home():
    return redirect('https://ceebryan.docs.apiary.io/#'), 301


@user.route('/users/orders', methods=['POST', 'GET'])
@token_require
def make_order(current_user):
    if request.method == 'POST':
        if not current_user:
            return make_response(jsonify({"status": "Failed", "message": "Please login to order"}), 401)
        user_data = request.get_json()
        meal_id = user_data.get('meal_id')
        user_id = current_user['user_id']
        time = datetime.datetime.now()
        quantity = user_data.get('quantity')
        if not quantity:
            quantity = 1
        from .models import place_order
        return place_order(meal_id, user_id, time, quantity)

    if not current_user:
        return make_response(jsonify({"status": "Failed",
                                      "message": "Login to view order history"}), 401)
    from app.api.v2.users.models import get_history
    return get_history(current_user['user_id'])