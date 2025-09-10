import os, sys, time, json
import psycopg

# Environment variables with defaults
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "secretpw")
DB_NAME = os.getenv("DB_NAME", "appdb")
TOP_N = int(os.getenv("APP_TOP_N", "5"))

def connect_with_retry(retries=10, delay=2):
    last_err = None
    for _ in range(retries):
        try:
            conn = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname=DB_NAME,
                connect_timeout=3,
            )
            return conn
        except Exception as e:
            last_err = e
            print("Waiting for database...", file=sys.stderr)
            time.sleep(delay)
    print("Failed to connect to Postgres:", last_err, file=sys.stderr)
    sys.exit(1)

def main():
    conn = connect_with_retry()
    with conn, conn.cursor() as cur:
        # Total number of trips
        cur.execute("SELECT COUNT(*) FROM trips;")
        total_trips = cur.fetchone()[0]

        # Average fare by city
        cur.execute("""
            SELECT city, AVG(fare)::numeric(10,2) AS avg_fare
            FROM trips
            GROUP BY city
            ORDER BY city;
        """)
        by_city = [{"city": c, "avg_fare": float(a)} for (c, a) in cur.fetchall()]

        # Top N trips by minutes (descending)
        cur.execute("""
            SELECT id, city, minutes, fare::float
            FROM trips
            ORDER BY minutes DESC, id ASC
            LIMIT %s;
        """, (TOP_N,))
        top_rows = cur.fetchall()
        top = [{"id": i, "city": c, "minutes": m, "fare": float(f)} for (i, c, m, f) in top_rows]

        summary = {
            "total_trips": int(total_trips),
            "avg_fare_by_city": by_city,
            "top_by_minutes": top
        }

        # Write to /out/summary.json
        os.makedirs("/out", exist_ok=True)
        with open("/out/summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Print to stdout
        print("=== Summary ===")
        print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()