class Drone(object):

    def __init__(self, id, number_of_product_types, x_coor, y_coor):
        self.id = id
        self.list_of_products = [0] * number_of_product_types
        self.current_load = 0
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.list_of_commands = []

    def load(self, warehouse, product, number_of_products):
        dist = self.move(warehouse.loc_x, warehouse.loc_y)
        self.pack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'L', str(warehouse.get_id()), str(product.get_id()), str(number_of_products)]) + '\n')
        return dist

    def deliver(self, order, product, number_of_products):
        dist = self.move(order.loc_x, order.loc_y)
        self.unpack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'D', str(order.get_id()), str(product.get_id()), str(number_of_products)]) + '\n')
        return dist

    def unload(self, warehouse, product, number_of_products):
        dist = self.move(warehouse.loc_x, warehouse.loc_y)
        self.unpack(product, number_of_products)
        self.list_of_commands.append(' '.join([str(self.id), 'U', str(warehouse.get_id()), str(product.get_id()), str(number_of_products)]) + '\n')
        return dist

    def unpack(self, product, number_of_products):
        self.list_of_products[product.get_id()] -= number_of_products
        assert (self.list_of_products[product.get_id()] >= 0)
        self.current_load -= number_of_products * product.get_weight()
        assert (self.current_load >= 0)

    def pack(self, product, number_of_products, max_load):
        self.list_of_products[product.get_id()] += number_of_products
        self.current_load += number_of_products * product.get_weight()
        assert(self.current_load <= max_load)

    def move(self, dest_x, dest_y):
        dist = int(ceil(((dest_x - self.x_coor) ** 2 + (dest_y - self.y_coor) ** 2) ** 0.5))
        self.x_coor = dest_x
        self.y_coor = dest_y
        return dist

    def wait(self, number_of_turns):
        self.list_of_commands.append(' '.join([str(self.id), 'W', str(number_of_turns)]) + '\n')

    def dump_commands(self):
        return self.list_of_commands
