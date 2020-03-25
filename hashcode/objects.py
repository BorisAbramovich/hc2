from collections import namedtuple

Location = namedtuple('Location', 'row col')

Item = namedtuple('Item', 'product_type quantity')

Warehouse = namedtuple('Warehouse', 'location items')

Order = namedtuple('Order', 'destination items')
