from typing import List

from location import Location
from warehouse import Warehouse
from order import Order
from drone import Drone

from basics.io import InputReader


class InputData(object):
    def __init__(self, rows, cols, drones_count, deadline, max_load, product_types, weights: List[int],
                 warehouses_count, warehouses: List[Warehouse], orders_count, orders: List[Order]):
        self.rows = rows
        self.cols = cols
        self.drones_count = drones_count
        first_warehouse_loc = warehouses[0].loc
        self.drones = [Drone(product_types, first_warehouse_loc, max_load) for _ in range(drones_count)]
        self.deadline = deadline
        self.max_load = max_load
        self.product_types = product_types  # video size
        self.weights = weights
        self.warehouses_count = warehouses_count
        self.warehouses = warehouses
        self.orders_count = orders_count
        self.orders = orders

    @classmethod
    def _from_text(cls, text):
        inp = InputReader(text)
        rows, cols, drones, deadline, max_load = inp.ints(5)
        product_types = inp.ints(1)
        weights = inp.ints(product_types)

        warehouses_count = inp.ints(1)
        warehouses = []
        for w in range(warehouses_count):
            row, col = inp.ints(2)
            quantities = inp.ints(product_types)
            warehouses.append(Warehouse(location=Location(row, col), list_of_products=quantities))

        orders_count = inp.ints(1)
        orders = []
        for order in range(orders_count):
            row, col = inp.ints(2)
            items_cnt = inp.ints(1)
            items_quantities = inp.ints(items_cnt)
            items = [items_quantities.count(i) for i in range(product_types)]
            orders.append(Order(destination=Location(row, col), product_quantities=items))

        return cls(rows, cols, drones, deadline, max_load, product_types, weights,
                   warehouses_count, warehouses, orders_count, orders)
