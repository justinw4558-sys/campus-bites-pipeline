# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery orders.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Setup

1. Clone the repository
2. Start the database:
   ```bash
   docker-compose up -d
   ```
3. The database will automatically create the `orders` table and load the CSV data on first startup.

## Connect to the Database

**Interactive SQL shell:**
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

**Connection details (for GUI tools like DBeaver, pgAdmin):**
- Host: `localhost`
- Port: `5432`
- Database: `campus_bites`
- Username: `postgres`
- Password: `postgres`

## Sample Queries

```sql
-- Count all orders
SELECT COUNT(*) FROM orders;

-- Orders by cuisine type
SELECT cuisine_type, COUNT(*) as order_count
FROM orders
GROUP BY cuisine_type
ORDER BY order_count DESC;

-- Average order value by customer segment
SELECT customer_segment, ROUND(AVG(order_value), 2) as avg_value
FROM orders
GROUP BY customer_segment;
```

## Stop the Database

```bash
docker-compose down
```

To also delete the data volume (reset everything):
```bash
docker-compose down -v
```
