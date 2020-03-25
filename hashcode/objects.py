from collections import namedtuple

Location = namedtuple('Location', 'row col')

Warehouse = namedtuple('Warehouse', 'location items')

Order = namedtuple('Order', 'destination items')
