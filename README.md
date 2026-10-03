# Amazon Aurora Read Replica Auto Scaling for Reporting Load

## Project Overview

This project demonstrates how **Amazon Aurora PostgreSQL Read Replica Auto Scaling** can be used to handle variable reporting and read-heavy database workloads.

The system uses an Amazon Aurora PostgreSQL cluster with a writer instance and reader instances. An **Aurora Auto Scaling policy** monitors the average CPU utilization of Aurora Replicas and automatically adds or removes reader instances according to the configured scaling conditions.

The main goal is to reduce the impact of increasing reporting workloads while avoiding unnecessary reader instances during periods of low activity.

---

## Objectives

- Create an Amazon Aurora PostgreSQL database cluster.
- Create and configure an Aurora reader instance.
- Store sample sales data in PostgreSQL.
- Execute read-intensive reporting queries.
- Monitor Aurora database and replica metrics.
- Configure Aurora Replica Auto Scaling.
- Generate additional reporting workload.
- Observe scaling behavior using Amazon RDS and Amazon CloudWatch.
- Document the complete implementation and results.

---

## AWS Services and Tools

### AWS Services

- Amazon Aurora PostgreSQL
- Amazon RDS
- Amazon RDS Auto Scaling
- Amazon CloudWatch
- AWS IAM
- AWS CLI

### Development and Database Tools

- PostgreSQL
- pgAdmin 4
- SQL Shell (psql)
- Python
- Git
- GitHub

---

## System Architecture

```text
                    Reporting Application
                            |
                            | Read Queries
                            v
                  Amazon Aurora PostgreSQL
                            |
                 +----------+----------+
                 |                     |
                 v                     v
             Writer                  Reader
          Aurora Instance        Aurora Reader
                                       |
                                       v
                              Reporting Workload
                                       |
                                       v
                              CloudWatch Metrics
                                       |
                                       v
                         Aurora Replica Auto Scaling
                                       |
                         +-------------+-------------+
                         |                           |
                    Add Reader                  Remove Reader
                  when workload               when workload
                     increases                   decreases
```

---

## Project Structure

```text
amazon-aurora-read-replica-autoscaling/
│
├── aws/
│   └── AWS configuration and project documentation
│
├── database/
│   ├── 01_create_tables.sql
│   ├── 02_insert_sample_data.sql
│   └── 03_reporting_queries.sql
│
├── load-test/
│   └── generate_load.py
│
├── screenshots/
│   └── Project screenshots
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 1. Aurora PostgreSQL Setup

An Amazon Aurora PostgreSQL database cluster is created in the AWS Management Console.

The cluster contains:

- One Aurora Writer instance
- One or more Aurora Reader instances
- Aurora PostgreSQL database engine
- Aurora cluster endpoints for writer and reader connections

The reader endpoint is used for read/reporting workloads.

---

# 2. Database Schema

The project uses a simple `sales` table for generating reporting workloads.

```sql
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL
);
```

### Table Columns

| Column | Description |
|---|---|
| `id` | Unique sales record ID |
| `product_id` | Product identifier |
| `amount` | Sale amount |
| `sale_date` | Date of sale |

---

# 3. Sample Data

Sample sales records are inserted into the Aurora PostgreSQL database.

Example:

```sql
INSERT INTO sales (product_id, amount, sale_date) VALUES
(1, 500.00, CURRENT_DATE),
(2, 750.00, CURRENT_DATE),
(3, 900.00, CURRENT_DATE),
(4, 1200.00, CURRENT_DATE),
(5, 800.00, CURRENT_DATE),
(2, 1100.00, CURRENT_DATE),
(3, 450.00, CURRENT_DATE),
(4, 650.00, CURRENT_DATE);
```

---

# 4. Reporting Queries

The project uses aggregation queries to simulate reporting workloads.

### Sales by Product

```sql
SELECT
    product_id,
    SUM(amount) AS total_sales
FROM sales
GROUP BY product_id
ORDER BY total_sales DESC;
```

### Daily Sales

```sql
SELECT
    sale_date,
    SUM(amount) AS daily_sales
FROM sales
GROUP BY sale_date
ORDER BY sale_date;
```

### Overall Sales Statistics

```sql
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_sale
FROM sales;
```

---

# 5. Aurora Reader Auto Scaling

An Aurora Replica Auto Scaling policy is configured for the Aurora cluster.

The scaling policy monitors:

**Average CPU utilization of Aurora Replicas**

Example target:

```text
Target CPU utilization: 60%
```

When the reporting workload increases and the configured scaling conditions are met, Aurora can add reader instances.

When the workload decreases and the configured scale-in conditions are met, Aurora can remove reader instances.

---

# 6. Monitoring

Amazon RDS and Amazon CloudWatch are used to monitor the database.

Important metrics include:

- CPU utilization
- Database load
- Database connections
- Read activity
- Number of Aurora replicas
- Replica CPU utilization

The monitoring dashboard is used to observe the effect of the reporting workload on Aurora reader instances.

---

# 7. Load Testing

A Python script is included to generate repeated reporting queries.

File:

```text
load-test/generate_load.py
```

The script repeatedly executes aggregation queries against the database to simulate a read-heavy reporting workload.

The workload is intended to increase activity on the Aurora reader and provide a practical demonstration of the auto-scaling configuration.

---

# 8. Testing Procedure

The project can be tested using the following sequence:

### Step 1
Verify that the Aurora cluster and reader instance are available.

### Step 2
Connect to Aurora PostgreSQL using `psql` or pgAdmin 4.

### Step 3
Create the `sales` table.

### Step 4
Insert the sample sales data.

### Step 5
Execute the reporting queries and verify the results.

### Step 6
Verify the Aurora Replica Auto Scaling policy.

### Step 7
Open Amazon RDS monitoring and observe the reader metrics.

### Step 8
Run the Python reporting workload generator.

### Step 9
Observe the Aurora reader CPU utilization and database load.

### Step 10
Observe whether Aurora Replica Auto Scaling adds or removes reader instances according to the configured policy and scaling conditions.

---

# 9. Expected Behavior

When reporting activity increases:

```text
Increased reporting queries
          ↓
Higher reader workload
          ↓
Higher replica CPU utilization
          ↓
CloudWatch/RDS monitoring
          ↓
Auto Scaling evaluates policy
          ↓
Additional Aurora reader
```

When reporting activity decreases:

```text
Lower reporting workload
          ↓
Lower reader CPU utilization
          ↓
Auto Scaling evaluates policy
          ↓
Unnecessary reader may be removed
```

Actual scaling depends on the configured policy, cooldown periods, workload intensity, and AWS service behavior.

---

# 10. Results

The following observations should be recorded during the final experiment:

| Parameter | Before Load | During Load | After Load |
|---|---|---|---|
| Number of Readers | To be measured | To be measured | To be measured |
| Reader CPU Utilization | To be measured | To be measured | To be measured |
| Database Load | To be measured | To be measured | To be measured |
| Reporting Query Activity | Normal | High | Normal |
| Auto Scaling Action | None/Initial | To be observed | To be observed |

Screenshots of the actual AWS console results should be stored in the `screenshots` directory.

---

# 11. Project Outcome

This project demonstrates an AWS database architecture for handling variable read-heavy reporting workloads using Amazon Aurora PostgreSQL and Aurora Replica Auto Scaling.

The implementation combines:

- Aurora PostgreSQL
- Read replicas
- Reporting queries
- CloudWatch/RDS monitoring
- Automatic replica scaling
- Python-based workload generation

The project provides a practical demonstration of how database read capacity can be dynamically adjusted according to workload requirements.

---

# 12. Repository

GitHub repository:

**amazon-aurora-read-replica-autoscaling**

The repository contains the SQL scripts, workload generator, AWS documentation, screenshots, and project documentation required to reproduce and demonstrate the project.

---

## Author

**Srivathsav**

B.Tech Computer Science and Engineering

## License

This project is created for educational and academic purposes.