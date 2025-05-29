import os
import pandas as pd
import random
from datetime import timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATA_DIR, exist_ok=True)

num_orders = 300
num_bases = 8
num_vendors = 10
supply_categories = [
    "Food", "Medical Supplies",
    "Fuel", "Vehicles", "Ammunition", "Communication Equipment"
]
bases = [fake.city() for _ in range(num_bases)]
vendors = [fake.company() for _ in range(num_vendors)]

def random_date_between(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

supply_orders = []
for i in range(num_orders):
    order_date = fake.date_between(start_date='-90d', end_date='-10d')
    expected_delivery = order_date + timedelta(days=random.randint(5, 30))
    base = random.choice(bases)
    vendor = random.choice(vendors)
    category = random.choice(supply_categories)
    units = random.randint(20, 1000)
    unit_cost = random.uniform(100, 2000)
    total_cost = round(units * unit_cost, 2)
    priority = random.choice(["Routine", "Urgent", "Emergency"])
    requester = fake.name()

    supply_orders.append({
        "order_id": f"ORD-{1000+i}",
        "order_date": order_date,
        "base": base,
        "vendor": vendor,
        "supply_category": category,
        "units_ordered": units,
        "unit_cost": round(unit_cost, 2),
        "total_cost": total_cost,
        "priority": priority,
        "requested_by": requester,
        "expected_delivery_date": expected_delivery
    })

supply_deliveries = []
for order in supply_orders:
    delay_days = random.choice([0, 1, 2, 5, -1, -2])
    actual_delivery = order["expected_delivery_date"] + timedelta(days=delay_days)
    delivery_method = random.choice(["Truck", "Helicopter", "Convoy", "Chartered Freight"])
    route_risk = random.choices(
    ["Low", "Medium", "High"],
    weights=[4, 1, 5], 
)[0]

    supply_deliveries.append({
        "order_id": order["order_id"],
        "vendor": order["vendor"],
        "base": order["base"],
        "supply_category": order["supply_category"],
        "expected_delivery_date": order["expected_delivery_date"],
        "actual_delivery_date": actual_delivery,
        "delay_days": (actual_delivery - order["expected_delivery_date"]).days,
        "delivery_method": delivery_method,
        "route_risk_level": route_risk
    })

inventory_records = []
tragic_supply_added = False 

for base in bases:
    for category in supply_categories:
        if category in ["Food","Fuel"] and not tragic_supply_added:
            daily_consumption = random.uniform(80, 120)
            days_remaining = round(random.uniform(5, 25), 1)
            inventory_level = int(daily_consumption * days_remaining)
            tragic_supply_added = True
        
        elif category in ["Ammunition"]:
            daily_consumption = random.uniform(5, 50)
            days_remaining = round(random.uniform(10, 45), 1)
            inventory_level = int(daily_consumption * days_remaining)

        elif category in ["Communication Equipment", "Vehicles", "Medical Supplies"]:
            daily_consumption = random.uniform(5, 50)
            days_remaining = random.uniform(61, 120)
            inventory_level = int(daily_consumption * days_remaining)

        else:
            inventory_level = random.randint(500, 10000)
            daily_consumption = random.uniform(5, 200)
            days_remaining = round(inventory_level / daily_consumption, 1)

        status = "Critical" if days_remaining < 30 else "Stable"
        last_updated = fake.date_between(start_date='-10d', end_date='today')

        inventory_records.append({
            "base": base,
            "supply_category": category,
            "inventory_units": inventory_level,
            "avg_daily_consumption": round(daily_consumption, 2),
            "days_remaining": round(days_remaining, 1),
            "inventory_status": status,
            "last_updated": last_updated
        })

budget_records = []
for base in bases:
    for category in supply_categories:
        allocated = random.randint(112300, 534679)
        spent = allocated * random.uniform(0.6, 1.2)
        budget_records.append({
            "base": base,
            "supply_category": category,
            "budget_allocated": allocated,
            "budget_spent": round(spent, 2),
            "budget_variance": round(spent - allocated, 2)
        })

pd.DataFrame(supply_orders).to_csv(os.path.join(DATA_DIR, "supply_orders.csv"), index=False)
pd.DataFrame(supply_deliveries).to_csv(os.path.join(DATA_DIR, "supply_deliveries.csv"), index=False)
pd.DataFrame(inventory_records).to_csv(os.path.join(DATA_DIR, "base_inventory_supply.csv"), index=False)
pd.DataFrame(budget_records).to_csv(os.path.join(DATA_DIR, "supply_budget.csv"), index=False)

print("Supply Orders, Deliveries, Inventory, and Budget datasets created in the 'dataset' directory.")