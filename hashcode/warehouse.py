from hashcode.location import Location


class Warehouse(object):

    def __init__(self, id, location: Location, list_of_products):
        self.id = id
        self.loc = location
        self.list_of_products = list_of_products

    def __str__(self):
       return 'Warehouse' + str(self.id) + ' in ' + str(self.loc)

    def get_id(self):
        return self.id

    def get_items(self, product_type, number_of_products):
        self.list_of_products[product_type] += number_of_products

    def give_items(self, product_type, number_of_products):
        self.list_of_products[product_type] -= number_of_products
        assert(self.list_of_products[product_type] >= 0)
