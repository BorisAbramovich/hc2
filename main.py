from hashcode import PROJECT_DIR
from hashcode.location import dist
from hashcode.product import Product
from hashcode.input_data import InputData
from basics import read
import os.path


def main():
    path = 'redundancy.in'
    name = os.path.basename(path)
    input_data = InputData._from_text(read(os.path.join(PROJECT_DIR, 'input_files', name)))
    available_drones = [[] for _ in range(input_data.deadline)]
    available_drones[0] = [i for i in range(input_data.drones_count)]
    # for order in input_data.orders:
    #     print(order)
    input_data.orders = sorted(input_data.orders, key=lambda o: sum(o.list_of_missing_products.values()))
    for t in range(input_data.deadline):
        for d in available_drones[t]:
            used_drone = False
            drone = input_data.drones[d]
            for order in input_data.orders:
                if used_drone:
                    break
                for prod_idx in order.list_of_missing_products:
                    if used_drone:
                        break
                    # print('order' + str(order))
                    # print('product' + str(prod_idx))
                    if (not used_drone) and order.list_of_missing_products[prod_idx] > 0:
                        product = Product(prod_idx, input_data.weights[prod_idx])
                        warehouse_lst = sorted(input_data.warehouses,
                                               key=lambda w: dist(w.loc, drone.loc) + dist(w.loc, order.destination))
                        for w in warehouse_lst:
                            # print(w)
                            if w.list_of_products[prod_idx] > 0:
                                turns1 = 0
                                for specific_prod_idx in order.list_of_missing_products:
                                    product_spec = Product(specific_prod_idx, input_data.weights[specific_prod_idx])
                                    quantity = min(
                                        [
                                            w.list_of_products[specific_prod_idx],
                                            order.list_of_missing_products[specific_prod_idx],
                                            (input_data.max_load - drone.current_load) // product_spec.weight
                                        ]
                                    )
                                    if quantity > 0:
                                        order.supply(product_spec, quantity)
                                        turns1 += drone.load(w, product_spec, quantity)
                                        w.give_items(specific_prod_idx, quantity)
                                turns2 = 0
                                for idx, quan in enumerate(drone.list_of_products):
                                    if quan > 0:
                                        product_spec = Product(idx, input_data.weights[idx])
                                        turns2 += drone.deliver(
                                            order=order, product=product_spec, number_of_products=quan)

                                if t + turns1 + turns2 < input_data.deadline:
                                        available_drones[t + turns1 + turns2].append(d)
                                elif t + turns1 + turns2 > input_data.deadline:
                                    drone.list_of_commands = drone.list_of_commands[:-1]
                                used_drone = True

                                break
            for order in input_data.orders:
                order.clean()
            input_data.orders = [o for o in input_data.orders if len(o.list_of_missing_products) >0]
            input_data.orders = sorted(input_data.orders, key=lambda o: sum(o.list_of_missing_products.values()))
            if not used_drone and t < input_data.deadline - 1:
                available_drones[t+1].append(d)

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
    return 0


if __name__ == '__main__':
    print('Starting')
    main()
    print('Done')
