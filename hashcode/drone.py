class Drone(object):

    def __init__(self, number_of_product_types, initial_location, max_load):
        self.list_of_products = [0] * number_of_product_types
        self.current_load = 0
        self.loc = initial_location
        self.max_load = max_load

    def load(self, product_type, product_weight, number_of_products):
        assert self.current_load + number_of_products * product_weight <= self.max_load
        self.list_of_products[product_type] += number_of_products
        self.current_load += number_of_products * product_weight

    def deliver(self, new_location):
        self.loc = new_location

    def unload(self, product_type, product_weight, number_of_products):
        self.list_of_products[product_type] -= number_of_products
        assert(self.list_of_products[product_type] >= number_of_products)
        self.current_load -= number_of_products * product_weight

    def wait(self):
        pass
