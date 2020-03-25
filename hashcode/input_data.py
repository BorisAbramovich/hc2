from typing import List

from basics.io import InputReader
from hashcode.objects import *
import numpy as np


class InputData:
    def __init__(self, rows, cols, drones, deadline, max_load, product_types, weights: List[Int],
                 warehouses_count, warehouses: List[Warehouse], orders_count, orders: List[Order]):
        self.rows = rows
        self.cols = cols
        self.drones = drones
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
            warehouses.append(Warehouse(location=Location(row, col), items=quantities))

        orders_count = inp.ints(1)
        orders = []
        for order in range(orders_count):
            row, col = inp.ints(2)
            items_cnt = inp.ints(1)
            items_quantities = inp.ints(items_cnt)
            items = [items_quantities.count(i) for i in range(product_types)]
            orders.append(Order(location=Location(row, col), items=items))

        return cls(rows, cols, drones, deadline, max_load, product_types, weights,
                   warehouses_count, warehouses, orders_count, orders)
