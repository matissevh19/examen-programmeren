"""
===============================================================
Dodona – Inventory Management (Examen 19 november)
===============================================================

In deze oefening implementeer je een voorraadbeheersysteem met
behulp van stacks (LIFO). Producten worden beheerd in batches,
waarbij de laatst toegevoegde batch eerst wordt gebruikt.

Doel:
-----
Realistische voorraadoperaties simuleren waarbij consumptie en
herbevoorrading in batchvorm gebeuren.

----------------------------------------------------------------
Batch-klasse (1 punt)
----------------------------------------------------------------
Een Batch stelt één voorraadbatch voor met:

- quantity          → hoeveelheid in batch
- cost_per_unit     → aankoopkost per eenheid in deze batch

Methoden:
- __str__(): geeft Batch weer als:
    Batch(quantity=[q], cost_per_unit=[c])

----------------------------------------------------------------
Product-klasse (6 punten)
----------------------------------------------------------------
Een Product bevat:

- product_name          → naam van het product
- batches               → stack (lijst) van Batch-objecten (LIFO)
- holding_cost          → aanhoudingskost per eenheid
- stockout_penalty      → boete wanneer vraag niet kan geleverd worden

Methoden:
1. add_batch(quantity, cost_per_unit)
   Voegt een nieuwe batch toe bovenaan de stack. (push)

2. fulfill_demand(demand)
   Vult vraag in LIFO-volgorde:
   - gebruik de bovenste batch
   - indien te weinig: gebruik batch volledig en verwijder die (pop)
   - indien vraag volledig kan worden ingevuld → return 0
   - indien vraag NIET volledig kan worden ingevuld:
       return (onvervulde hoeveelheid) * stockout_penalty

3. calculate_holding_cost()
   Geeft totale holding cost terug:
       som(batch.quantity * holding_cost)

4. __str__()
   Print product + batches in correcte vorm:
   Product [naam]:
       Batch(quantity=..., cost_per_unit=...)
       Batch(quantity=..., cost_per_unit=...)
       ...

----------------------------------------------------------------
Inventory_Manager-klasse (11 punten)
----------------------------------------------------------------

Beheert meerdere producten in een dictionary:

self.products = { product_name: Product-object }

Methoden:

1. add_product(product_name, holding_cost, stockout_penalty)
   - voegt nieuw product toe
   - als product al bestaat → print:
        Product [product_name] already exists.

2. restock_product(product_name, quantity, cost_per_unit)
   - voegt nieuwe batch toe aan product
   - als product niet bestaat → print:
        Product [product_name] not found

3. simulate_demand(min_demand, max_demand)
   - genereert random vraag per product
   - standaard: min_demand=0, max_demand=20
   - return → dict { product_name : demand }

4. simulate_day(demand)
   - gebruikt fulfill_demand() per product
   - berekent holding_cost en stockout_cost
   - return: (total_holding_cost, total_stockout_cost)

5. save_to_csv(filename)
   - schrijft per batch naar CSV:
        product_name, batch_quantity, batch_cost_per_unit

6. load_from_csv(filename)
   - leest batches terug in
   - als product nog niet bestaat → maak nieuw Product
     met default holding_cost=1, stockout_penalty=1
   - voeg batch toe

7. print_inventory()
   - print alle producten en hun batches
   - gebruikte outputvorm:

Current Inventory:
Product Widget:
Batch(quantity=100, cost_per_unit=2.5)
Batch(quantity=50, cost_per_unit=2.0)

Product Gadget:
Batch(quantity=70, cost_per_unit=3.0)

----------------------------------------------------------------
MAIN-methode (2 punten)
----------------------------------------------------------------
Voeg een main toe die:

- minstens 2 producten toevoegt
- elk product heeft minstens 2 batches
- vraag simuleert
- één dag simuleert
- voorraad opslaat naar CSV
- voorraad print naar scherm

----------------------------------------------------------------
OPMERKINGEN:
----------------------------------------------------------------
- Gebruik uitsluitend LIFO-logica via append() en pop().
- Batches worden niet samengevoegd.
- CSV bevat geen headers volgens Dodona.
- Zorg dat __str__ correct werkt (veel punten!).
- Focus: correcte stack-operaties en correcte berekeningen.

===============================================================
"""

import csv
import random

# ============================================================
# BATCH CLASS — stelt één voorraadbatch voor
# ============================================================

class Batch:
    def __init__(self, quantity, cost_per_unit):
        # hoeveelheid van het product in deze batch
        self.quantity = quantity
        # kost per eenheid van deze batch (kan verschillen per batch)
        self.cost_per_unit = cost_per_unit

    def __str__(self):
        # correcte output zoals Dodona vereist
        return f"Batch(quantity={self.quantity}, cost_per_unit={self.cost_per_unit})"


# ============================================================
# PRODUCT CLASS — verzamelt batches in een STACK (LIFO)
# ============================================================

class Product:
    def __init__(self, product_name, holding_cost, stockout_penalty):
        self.product_name = product_name
        self.holding_cost = holding_cost          # kost per overgebleven eenheid/dag
        self.stockout_penalty = stockout_penalty  # boete per niet-geleverde eenheid
        self.batches = []                         # dit is onze STACK

    # -----------------------------------------
    # Batch toevoegen (push op LIFO-stack)
    # -----------------------------------------
    def add_batch(self, quantity, cost_per_unit):
        new_batch = Batch(quantity, cost_per_unit)
        self.batches.append(new_batch)  # LIFO → append duwt bovenaan

    # ------------------------------------------------------
    # Vraag invullen volgens LIFO (pop van de stack)
    # ------------------------------------------------------
    def fulfill_demand(self, demand):

        # zolang er vraag is en batches bestaan
        while demand > 0 and len(self.batches) > 0:

            top = self.batches[-1]  # bovenste batch

            # batch heeft meer dan genoeg voorraad
            if top.quantity > demand:
                top.quantity -= demand     # verminder voorraad
                return 0                   # geen stockout

            # batch heeft te weinig voorraad
            else:
                demand -= top.quantity     # verbruik de hele batch
                self.batches.pop()         # verwijder volledige batch (pop)

        # als we hier komen was er niet genoeg voorraad
        if demand > 0:
            return demand * self.stockout_penalty

        return 0

    # -----------------------------------------
    # Holding cost = som(batch.quantity × holding_cost)
    # -----------------------------------------
    def calculate_holding_cost(self):
        total = 0
        for batch in self.batches:
            total += batch.quantity * self.holding_cost
        return total

    # -----------------------------------------
    # Printweergave van het product + batches
    # -----------------------------------------
    def __str__(self):
        result = f"Product {self.product_name}:\n"
        for batch in self.batches:
            result += str(batch) + "\n"
        return result.rstrip("\n")


# ============================================================
# INVENTORY MANAGER CLASS — beheert meerdere producten
# ============================================================

class Inventory_Manager:
    def __init__(self):
        # dictionary: naam → Product-object
        self.products = {}

    # ---------------------------------------------------
    # Nieuw product toevoegen aan het systeem
    # ---------------------------------------------------
    def add_product(self, product_name, holding_cost, stockout_penalty):
        if product_name in self.products:
            print(f"Product {product_name} already exists.")
            return

        self.products[product_name] = Product(
            product_name, holding_cost, stockout_penalty
        )

    # ---------------------------------------------------
    # Restock = batch toevoegen aan bestaand product
    # ---------------------------------------------------
    def restock_product(self, product_name, quantity, cost_per_unit):
        if product_name not in self.products:
            print(f"Product {product_name} not found")
            return

        self.products[product_name].add_batch(quantity, cost_per_unit)

    # ---------------------------------------------------
    # Random vraag genereren (per product)
    # ---------------------------------------------------
    def simulate_demand(self, min_demand=0, max_demand=20):
        demands = {}

        for name in self.products:
            # willekeurige vraag per product
            demands[name] = random.randint(min_demand, max_demand)

        return demands

    # ---------------------------------------------------
    # 1 dag simuleren: verbruik + kosten
    # ---------------------------------------------------
    def simulate_day(self, demand_dict):

        total_holding_cost = 0
        total_stockout_cost = 0

        for name, demand in demand_dict.items():

            product = self.products[name]

            # stockout kost
            stockout_cost = product.fulfill_demand(demand)
            total_stockout_cost += stockout_cost

            # holding kost
            holding_cost = product.calculate_holding_cost()
            total_holding_cost += holding_cost

        return total_holding_cost, total_stockout_cost

    # ---------------------------------------------------
    # Voorraad opslaan in CSV (zonder header, Dodona-stijl)
    # ---------------------------------------------------
    def save_to_csv(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            for name, product in self.products.items():
                for batch in product.batches:
                    writer.writerow([
                        name,
                        batch.quantity,
                        batch.cost_per_unit
                    ])

    # ---------------------------------------------------
    # CSV terug inladen als voorraad
    # ---------------------------------------------------
    def load_from_csv(self, filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)

            for row in reader:
                name = row[0]
                quantity = int(row[1])
                cost_per_unit = float(row[2])

                # product bestaat nog niet → maak product met default costs = 1
                if name not in self.products:
                    self.products[name] = Product(name, 1, 1)

                # batch toevoegen aan product
                self.products[name].add_batch(quantity, cost_per_unit)

    # ---------------------------------------------------
    # Voorraad printen in exact het vereiste formaat
    # ---------------------------------------------------
    def print_inventory(self):
        print("Current Inventory:")
        for product in self.products.values():
            print(product)
            print()


# ============================================================
# MAIN → wat Dodona vraagt: 2 producten, 2 batches, simulatie
# ============================================================

def main():

    manager = Inventory_Manager()

    # Producten toevoegen
    manager.add_product("Widget", 1, 5)
    manager.add_product("Gadget", 1, 3)

    # Minstens 2 batches per product
    manager.restock_product("Widget", 100, 2.5)
    manager.restock_product("Widget", 50, 2.0)

    manager.restock_product("Gadget", 70, 3.0)
    manager.restock_product("Gadget", 30, 2.8)

    # Willekeurige vraag genereren
    demand = manager.simulate_demand()

    # Dag simuleren → holding + stockout cost
    holding, stockout = manager.simulate_day(demand)

    print("Holding cost today:", holding)
    print("Stockout cost today:", stockout)

    # Opslaan in CSV
    manager.save_to_csv("inventory.csv")

    # Voorraad tonen
    manager.print_inventory()


# ============================================================
# Uitvoeren wanneer script direct gerund wordt
# ============================================================

if __name__ == "__main__":
    main()


