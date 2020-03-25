from hashcode.location import Location
from math import ceil


class Drone(object):

    def __init__(self, id, number_of_product_types, initial_location, max_load):
        self.id = id
        self.list_of_products = [0] * number_of_product_types
        self.current_load = 0
        self.loc = initial_location
        self.max_load = max_load
        self.list_of_commands = []

    def load(self, warehouse, product, number_of_products):
        dist = self.move(warehouse.loc[0], warehouse.loc[1])
        self.pack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'L', str(warehouse.get_id()), str(product.type_id), str(number_of_products)]) + '\n')
        return dist + 1

    def deliver(self, order, product, number_of_products):
        dist = self.move(order.destination[0], order.destination[1])
        self.unpack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'D', str(order.get_id()), str(product.type_id), str(number_of_products)]) + '\n')
        return dist + 1

    def unload(self, warehouse, product, number_of_products):
        dist = self.move(warehouse.loc[0], warehouse.loc[1])
        self.unpack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'U', str(warehouse.get_id()), str(product.type_id), str(number_of_products)]) + '\n')
        return dist + 1

    def unpack(self, product, number_of_products):
        self.list_of_products[product.type_id] -= number_of_products
        assert (self.list_of_products[product.type_id] >= 0)
        self.current_load -= number_of_products * product.weight
        assert (self.current_load >= 0)

    def pack(self, product, number_of_products):
        self.list_of_products[product.type_id] += number_of_products
        self.current_load += number_of_products * product.weight
        assert(self.current_load <= self.max_load)

    def move(self, dest_x, dest_y):
        dist = int(ceil(((dest_x - self.loc[0]) ** 2 + (dest_y - self.loc[1]) ** 2) ** 0.5))
        self.loc = Location(dest_x, dest_y)
        return dist

    def wait(self, number_of_turns):
        self.list_of_commands.append(' '.join([str(self.id), 'W', str(number_of_turns)]) + '\n')

    def dump_commands(self):
        return self.list_of_commands
