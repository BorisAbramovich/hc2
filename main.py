from hashcode import PROJECT_DIR
from hashcode.output import write_output
from hashcode.product import Product
from hashcode.input_data import InputData
from basics import read
import os.path


def main():
    path = 'mother_of_all_warehouses.in'
    name = os.path.basename(path)
    input_data = InputData._from_text(read(os.path.join(PROJECT_DIR, 'input_files', name)))
    available_drones = [[] for _ in range(input_data.deadline)]
    available_drones[0] = [i for i in range(input_data.drones_count)]
    for t in range(input_data.deadline):
        for d in available_drones[t]:
            drone = input_data.drones[d]
            for order in input_data.orders:
                for prod_idx in range(len(order.list_of_missing_products)):
                    if order.list_of_missing_products[prod_idx] > 0:
                        product = Product(prod_idx, input_data.weights[prod_idx])
                        for w in input_data.warehouses:
                            if w.list_of_products[prod_idx] > 0:
                                quantity = min(
                                    [
                                        w.list_of_products[prod_idx],
                                        order.list_of_missing_products[prod_idx],
                                        input_data.max_load // product.weight
                                    ]
                                )
                                turns1 = drone.load(w, product, quantity)
                                w.give_items(prod_idx, quantity)
                                order.supply(product, quantity)
                                turns2 = drone.deliver(order=order, product=product, number_of_products=quantity)
                                if t + turns1 + turns2 < input_data.deadline:
                                    available_drones[t + turns1 + turns2].append(d)

    out_stream = ""
    count = 0
    for d in input_data.drones:
        commands = d.dump_commands()
        out_stream += "".join(commands)
        count += len(commands)
    out_stream = str(count) + "\n" + out_stream
    out_path = os.path.join(PROJECT_DIR, 'outputs', name[:-3] + '.out')
    with open(out_path, 'w+') as out_file:
        out_file.write(out_stream)
    return out_stream


if __name__ == '__main__':
    print('Starting')
    main()
    print('Done')
