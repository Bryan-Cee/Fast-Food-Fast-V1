"""Holds the dummy data for the application"""


class OrderFood:
    """Create a new list to store user data"""

    def __init__(self):
        self.all_orders = []
        self.menu = []

    def get_all_orders(self):
        """Create a new list to store the orders"""
        return self.all_orders

    def current_menu(self):
        """Create a new list to store the menu items"""
        return self.menu


