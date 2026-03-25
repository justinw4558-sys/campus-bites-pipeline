# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- Python virtual environment: `.venv/` — use `.venv/bin/python` and `.venv/bin/pip`
- Database runs in Docker — always ensure the container is up before running scripts

## Common Commands

```bash
# Start the database
docker compose up -d

# Stop the database
docker compose down

# Reset the database (deletes all data)
docker compose down -v

# Install Python dependencies
.venv/bin/pip install pandas psycopg2-binary

# Load CSV data into the database
.venv/bin/python load_data.py

# Open an interactive SQL shell
docker exec -it campus_bites_db psql -U postgres -d campus_bites

# Run a quick SQL query
docker exec campus_bites_db psql -U postgres -d campus_bites -c "SELECT COUNT(*) FROM orders;"
```

## Architecture

This is a single-table local analytics pipeline:

- `docker-compose.yml` — runs a PostgreSQL 16 container (`campus_bites_db`) on `localhost:5432`, mounts `./data` into the container at `/data`
- `load_data.py` — creates the `orders` table (if not exists) and bulk-loads `data/campus_bites_orders.csv` using `psycopg2`; idempotent via `ON CONFLICT (order_id) DO NOTHING`
- `data/campus_bites_orders.csv` — source data (1,132 rows of campus food delivery orders)

## Database Connection

- Host: `localhost`, Port: `5432`, Database: `campus_bites`, User: `postgres`, Password: `postgres`
- The named volume `postgres_data` persists data across container restarts; `docker compose down -v` removes it
