class Warehouse(self):

    def __init__(self, loc_x, loc_y, list_of_products):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.list_of_products = list_of_products

    def get_items(self, product_type, number_of_products):
        self.list_of_products[product_type] += number_of_products

    def give_items(self, product_type, number_of_products):
        self.list_of_products[product_type] -= number_of_products
        assert(self.list_of_products[product_type] >= 0)