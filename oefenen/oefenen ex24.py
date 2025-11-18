import csv


class Batch:
    def __init__(self, quantity, cost_per_unit):
        self.quantity = quantity
        self.cost_per_unit = cost_per_unit

    def __str__(self):
        return f"Batch(quantity={self.quantity}, cost_per_unit={self.cost_per_unit})"

class Product:
    def __init__(self, product_name, holding_cost, stockout_penalty):
        self.product_name = product_name
        self.holding_cost = holding_cost
        self.stockout_penalty = stockout_penalty
        self.batches = []

    def add_batch(self, quantity, cost_per_unit):
        new_batch = Batch(quantity, cost_per_unit)
        self.batches.append(new_batch)

    def fulfill_demand(self, demand):
        while demand > 0 and len(self.batches) > 0:
            top_batch = self.batches[-1]
            if top_batch.quantity > demand:
                top_batch.quantity -= demand
                demand = 0
                return 0
            else:
                demand -= top_batch.quantity
                self.batches.pop()
        if demand > 0:
            return demand * self.stockout_penalty

    def calculate_holding_cost(self):
        total = 0
        for batch in self.batches:
            total += (batch.quantity * self.holding_cost)
        return total

    def __str__(self):
        result = f"Product {self.product_name}:\n"
        for batch in self.batches:
            result += str(batch) + "\n"
        return result.strip()

class Inventory_Manager:
    def __init__(self):
        self.products = {}

    def add_product(self, product_name, holding_cost, stockout_penalty):
        if product_name in self.products:
            print(f"Product [{product_name}] already exists.")
            return
        self.products[product_name] = Product(product_name, holding_cost, stockout_penalty)

    def restock_product(self, product_name, quantity, cost_per_unit):
        if product_name not in self.products:
            print(f"Product [{product_name}] not found")
            return
        self.products[product_name].add_batch(quantity, cost_per_unit)

    def simulate_demand(self, min_demand = 0, max_demand = 20):
        import random
        demands = {}
        for name in self.products:
            demands[name] = random.randint(min_demand, max_demand)
        return demands

    def simulate_day(self, demand_dict):
        total_holding_cost = 0
        total_stockout_cost = 0

        for name, demand in demand_dict.items():
            product = self.products[name]

            stockout_cost = product.fulfill_demand(demand)
            holding_cost = product.calculate_holding_cost()

            total_holding_cost += holding_cost
            total_stockout_cost += stockout_cost
        return total_holding_cost, total_stockout_cost

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for name, product in self.products.items():
                for batch in product.batches:
                    writer.writerow([name, batch.quantity, batch.cost_per_unit])

    def load_from_csv(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name = row[0]
                quantity = int(row[1])
                cost_per_unit = float(row[2])

                if name not in self.products:
                    self.products[name] = Product(name, 1, 1)
                self.products[name].add_batch(quantity, cost_per_unit)

    def print_inventory(self):
        print("Current inventory:")
        for product in self.products.values():
            print(product)
            print


def main():
    manager = Inventory_Manager()

    manager.add_product("Widget", 1, 5)
    manager.add_product("Gadget", 1, 3)

    manager.restock_product("Widget", 100, 2.5)
    manager.restock_product("Widget", 50, 2.0)

    manager.restock_product("Gadget", 70, 3.0)
    manager.restock_product("Gadget", 30, 2.8)

    demand = manager.simulate_demand()

    manager.simulate_day(demand)

    manager.save_to_csv("inventory.csv")

    manager.print_inventory()

if __name__ == "__main__":
    main()







