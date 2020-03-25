from hashcode.location import Location


class Order(object):
    def __init__(self, id, destination: Location, product_quantities):
        """order_list is a list of (product, num_items) tuples"""
        self.destination = destination
        self.list_of_missing_products = product_quantities
        self.id = id

    def __str__(self):
        return 'order_id=' + str(self.id) + ' missing_list' + str(self.list_of_missing_products)

    def supply(self, product, num_of_items):
        self.list_of_missing_products[product.type_id] -= num_of_items
        assert self.list_of_missing_products[product.type_id] >= 0

    def clean(self):
        keys = list(self.list_of_missing_products.keys())
        for k in keys:
            if self.list_of_missing_products[k] == 0:
                del self.list_of_missing_products[k]

    def get_id(self):
        return self.id