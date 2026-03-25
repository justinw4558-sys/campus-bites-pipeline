import pandas as pd
import psycopg2

# --- Database connection settings ---
# These match the credentials defined in docker-compose.yml
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# --- Path to the source CSV file ---
CSV_PATH = "data/campus_bites_orders.csv"

# --- DDL: Table definition ---
# IF NOT EXISTS means this is safe to run even if the table already exists
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE NOT NULL,
    order_time          TIME NOT NULL,
    customer_segment    VARCHAR(50) NOT NULL,
    order_value         DECIMAL(10, 2) NOT NULL,
    cuisine_type        VARCHAR(50) NOT NULL,
    delivery_time_mins  INTEGER NOT NULL,
    promo_code_used     VARCHAR(3) NOT NULL,
    is_reorder          VARCHAR(3)
);
"""

def load():
    # --- Read CSV into a DataFrame ---
    df = pd.read_csv(CSV_PATH)

    # --- Open a connection and cursor to the database ---
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # --- Create the orders table if it doesn't already exist ---
    cur.execute(CREATE_TABLE)

    # --- Convert DataFrame rows to a list of tuples for bulk insert ---
    rows = [tuple(row) for row in df.itertuples(index=False)]

    # --- Insert all rows; skip duplicates based on order_id ---
    cur.executemany(
        """
        INSERT INTO orders (order_id, order_date, order_time, customer_segment,
                            order_value, cuisine_type, delivery_time_mins,
                            promo_code_used, is_reorder)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
        """,
        rows,
    )

    # --- Commit the transaction and close the connection ---
    conn.commit()
    print(f"Loaded {cur.rowcount} rows into orders.")
    cur.close()
    conn.close()

# --- Entry point: only runs when executed directly, not when imported ---
if __name__ == "__main__":
    load()
