## Data Model & Dictionary

### 1. Logical Data Model Overview

**Entity Relationship Summary:**
- **Bases** (1) → (M) **Emergency Requests** → (1) **Vendor Deliveries**
- **Bases** (1) → (M) **Inventory Status** (by supply category)
- **Bases** (1) → (M) **Budget Ledger** (by supply category) 
- **Vendors** (1) → (M) **Vendor Deliveries**
- **Supply Categories** referenced across all operational tables

**Key Relationships:**
- Emergency requests link to deliveries via order_id
- Inventory and budget tracked at base + supply_category level
- Vendor performance measured through delivery records

**Core Tables:**
- **Emergency Request**: Core table tracking origin, type, priority, and status of critical procurement events  
- **Delivery Info**: Links order IDs with vendors and timestamps  
- **Inventory Status**: Tracks stock levels and usage rates by base and category  
- **Budget Ledger**: Records allocations and expenditures by base/category  
- **Vendor**: Master list of registered suppliers  

---

### 2. Synthetic Data Generation Method

The dataset was generated using Python and the Faker library for simulation.

Realistic values were created for vendor names, base locations, and delivery patterns.

Relationships between orders, inventory, and budget were manually structured to resemble military supply workflows.

Date ranges span approximately the last 90 days.

Logic for delay, consumption, budget overrun, and risk scoring was injected based on probability distributions.

---

### 3. SQL DDL Schema

```sql
CREATE TABLE bases (
 base VARCHAR(100) PRIMARY KEY
);

CREATE TABLE vendors (
 vendor VARCHAR(100) PRIMARY KEY
);

CREATE TABLE supply_categories (
 supply_category VARCHAR(100) PRIMARY KEY
);

CREATE TABLE emergency_requests (
 request_id VARCHAR(50) PRIMARY KEY,
 base VARCHAR(100) REFERENCES bases(base),
 supply_category VARCHAR(100) REFERENCES supply_categories(supply_category),
 units_requested INT NOT NULL,
 priority VARCHAR(20) CHECK (priority IN ('Routine', 'Urgent', 'Emergency')),
 request_date DATE NOT NULL,
 status VARCHAR(20) CHECK (status IN ('Pending', 'Approved', 'Delivered'))
);

CREATE TABLE vendor_deliveries (
 order_id VARCHAR(50) PRIMARY KEY,
 vendor VARCHAR(100) REFERENCES vendors(vendor),
 base VARCHAR(100) REFERENCES bases(base),
 supply_category VARCHAR(100) REFERENCES supply_categories(supply_category),
 expected_delivery_date DATE NOT NULL,
 actual_delivery_date DATE NOT NULL,
 delay_days INT,
 route_risk_level VARCHAR(20) CHECK (route_risk_level IN ('Low', 'Medium', 'High'))
);

CREATE TABLE base_inventory_supply (
 base VARCHAR(100) REFERENCES bases(base),
 supply_category VARCHAR(100) REFERENCES supply_categories(supply_category),
 inventory_units INT NOT NULL,
 avg_daily_consumption FLOAT NOT NULL,
 days_remaining FLOAT,
 last_updated DATE NOT NULL,
 PRIMARY KEY (base, supply_category)
);

CREATE TABLE supply_budget (
 base VARCHAR(100) REFERENCES bases(base),
 supply_category VARCHAR(100) REFERENCES supply_categories(supply_category),
 budget_allocated FLOAT NOT NULL,
 budget_spent FLOAT NOT NULL,
 budget_variance FLOAT,
 PRIMARY KEY (base, supply_category)
);
```
---

### 4. Data Dictionary (Field-Level Schema)

#### Table: emergency_requests

| Field Name | Type | Description | Required | Example |
|---|---|---|---|---|
| request_id | String | Unique request identifier | Yes | ERQ-1023 |
| base | String | Originating base/location | Yes | Camp Delta |
| supply_category | String | Type of supply (Medical, Fuel, etc.) | Yes | Medical |
| units_requested | Integer | Quantity of items requested | Yes | 300 |
| priority | String | Request urgency (Routine/Urgent/Emergency) | Yes | Emergency |
| request_date | Date | Date the request was submitted | Yes | 2025-05-01 |
| status | String | Current status (Pending, Approved, Delivered) | Yes | Approved |

#### Table: vendor_deliveries

| Field Name | Type | Description | Required | Example |
|---|---|---|---|---|
| order_id | String | Unique order reference | Yes | ORD-2049 |
| vendor | String | Vendor fulfilling the order | Yes | Global Logistics Ltd. |
| base | String | Base receiving the delivery | Yes | Camp Kilo |
| supply_category | String | Type of supply being delivered | Yes | Medical |
| expected_delivery_date | Date | Scheduled delivery date | Yes | 2025-05-10 |
| actual_delivery_date | Date | Date goods were actually delivered | Yes | 2025-05-13 |
| delay_days | Integer | Days late (positive) or early (negative) vs expected | Auto | 3 |
| route_risk_level | String | Security risk assessment for transport route | Yes | Medium |

#### Table: base_inventory_supply

| Field Name | Type | Description | Required | Example |
|---|---|---|---|---|
| base | String | Base name | Yes | Camp Bravo |
| supply_category | String | Supply type tracked | Yes | Fuel |
| inventory_units | Integer | Current units in stock | Yes | 1200 |
| avg_daily_consumption | Float | Average daily use | Yes | 45.2 |
| days_remaining | Float | Inventory coverage forecast | Auto | 26.5 |
| last_updated | Date | Date inventory was last refreshed | Yes | 2025-05-19 |

#### Table: supply_budget

| Field Name | Type | Description | Required | Example |
|---|---|---|---|---|
| base | String | Base name | Yes | Camp Juliet |
| supply_category | String | Category under budget | Yes | Communication Equip. |
| budget_allocated | Float | Total budget allocated | Yes | 50000.00 |
| budget_spent | Float | Actual spend to date | Yes | 57289.68 |
| budget_variance | Float | Difference between spent and allocated | Auto | 7289.68 |

---

### 5. Data Validation Rules

#### Business Rules

- `days_remaining` = `inventory_units` / `avg_daily_consumption`
- `delay_days` = `actual_delivery_date` - `expected_delivery_date`
- `budget_variance` = `budget_spent` - `budget_allocated`
- Emergency requests must have `priority` = 'Emergency'
- Inventory alerts triggered when `days_remaining` < 35

#### Data Quality Checks

- All delivery dates must be within last 90 days
- `avg_daily_consumption` must be > 0
- `inventory_units` cannot be negative
- Route risk levels restricted to predefined values
- Budget allocations must be positive values

---

### 6. Governance Considerations

#### Data Ownership

- **Logistics Systems Section**: procurement, inventory, and budget tables
- **Base-level logistics**: request records and local inventory updates
- **Vendor Management Office**: vendor master data and performance metrics

#### Data Quality Standards

- Inventory updates required within 24 hours of stock changes
- Delivery confirmations must be logged within 2 hours of receipt
- Budget variance reconciliation performed weekly

#### Audit Trail Requirements

- All emergency requests require approval workflow tracking
- Vendor performance SLA compliance monitored in real-time
- Budget variance explanations mandatory for >15% overruns

#### Retention Policy

- Emergency request logs and delivery records retained for 3 years
- Inventory snapshots retained monthly
- Budget reconciliation records retained for 7 years

#### Security Classification

- All datasets marked RESTRICTED – Operational
- Access governed by role-based control at system level

#### Access Controls

- **Read access**: All logistics personnel, base commanders
- **Write access**: Designated logistics officers only
- **Admin access**: Systems administrators and data stewards

### 7. Performance & Technical Notes

#### Indexing Strategy

- Primary indexes on all primary keys
- Secondary indexes on: `base`, `vendor`, `supply_category`, `request_date`
- Composite index on (`base`, `supply_category`) for inventory lookups

#### Data Volume Estimates

- ~500 emergency requests per month
- ~2,000 vendor deliveries per month
- ~200 base-category inventory records (updated daily)
- ~200 budget line items (updated weekly)

#### Refresh Frequency

- **Real-time**: Emergency requests, delivery confirmations
- **Daily**: Inventory levels, consumption rates
- **Weekly**: Budget variance calculations
- **Monthly**: Vendor performance metrics