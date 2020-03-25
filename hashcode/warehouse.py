from location import Location


class Warehouse(object):

    def __init__(self, location: Location, list_of_products):
        self.loc = location
        self.list_of_products = list_of_products

    def get_items(self, product_type, number_of_products):
        self.list_of_products[product_type] += number_of_products

    def give_items(self, product_type, number_of_products):
        self.list_of_products[product_type] -= number_of_products
        assert(self.list_of_products[product_type] >= 0)
