class order:
    def __init__(self, id, number_of_product_types, order_list, loc_x, loc_y):
        "order_list is a list of (product, num_items) tuples"
        self.list_of_missing_products = [0] * number_of_product_types
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.id = id
        for product in order_list:
            (product, num_of_items) = product
            self.list_of_missing_products[product.get_id] += num_of_items

    def supply(self, product, num_of_items):
        self.list_of_missing_products[product.get_id()] -= num_of_items
        assert self.list_of_missing_products[product.get_id()] >= 0
    def get_id(self):
        return self.id