from flask import Blueprint, request, jsonify
from app.api.V1.models import OrderFood

V1 = Blueprint('v1', __name__, url_prefix='/api/v1')

NEW_ORDER = OrderFood().get_all_orders()
MENU = OrderFood().current_menu()


@V1.route('/', methods=['GET'])
def hello():
    """Home page"""
    return 'Welcome to Fast Food Fast', 200


@V1.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    """Posting and getting new orders"""
    if request.method == 'POST':
        if not NEW_ORDER:
            order_details = {'order_id': 1,
                             'foodname': request.json['foodname'],
                             'status': 'new order'}
        else:
            order_details = {'order_id': NEW_ORDER[-1]['order_id'] + 1,
                             'foodname': request.json['foodname'],
                             'status': 'new order'}

        foodname = [food for food in MENU if order_details['foodname'] == food['foodname']]
        if not foodname:
            return "Invalid order, the food you ordered is not in the menu", 400
        NEW_ORDER.append(order_details)
        return 'Order for {} has been received'.format(order_details['foodname']), 201

    if not NEW_ORDER:
        return 'No orders yet'
    return jsonify({'Orders': NEW_ORDER})


@V1.route('/orders/<int:orderid>', methods=['GET', 'PUT'])
def get_specific_order(orderid):
    """Getting specific order and updating the status"""
    ids = [order for order in NEW_ORDER if order["order_id"] == orderid]
    if not ids:
        return "The order was not found", 404

    if request.method == 'PUT':
        status = request.json["status"]
        if status in("rejected", "accepted"):
            ids[0]["status"] = request.json["status"]
            return 'Order id {} has been updated'.format(ids[0]["order_id"])

        return 'You can only update the status as rejected or accepted'

    return jsonify({"Order": ids})


@V1.route("/menu", methods=['POST', 'GET'])
def add_meal_to_menu():
    """Adding meals to menu and viewing them"""
    if request.method == 'POST':
        mealname = [meal[key] for meal in MENU for key in meal.keys() if key == 'foodname']
        if request.json['foodname'] not in mealname:
            if not MENU:
                meal = {'order_id': 1,
                        "foodname": request.json['foodname'],
                        "price": request.json['price']}
            else:
                meal = {'order_id': MENU[-1]['order_id'] + 1,
                        "foodname": request.json['foodname'],
                        "price": request.json['price']}

            MENU.append(meal)

            return 'Meal added', 201

        return 'Meal is already in the menu', 400

    if not MENU:
        return 'No meals have been added to the menu'
    return jsonify({"Menu": MENU})
