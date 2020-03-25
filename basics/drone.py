class Drone(object):

    def __init__(self, number_of_product_types, x_coor, y_coor):
        self.list_of_products = [0] * number_of_product_types
        self.current_load = 0
        self.x_coor = x_coor
        self.y_coor = y_coor

    def load(self, product, number_of_products):
        self.list_of_products[product.get_id()] += number_of_products
        self.current_load += number_of_products * product.get_weight()

    def deliver(self, dest_x, dest_y):
        self.x_coor = dest_x
        self.y_coor = dest_y

    def unload(self, product, number_of_products):
        self.list_of_products[product.get_id()] -= number_of_products
        assert(self.list_of_products[product.get_id()] >= 0)
        self.current_load -= number_of_products * product.get_weight()
        assert (self.current_load >= 0)

    def wait(self):
        pass

