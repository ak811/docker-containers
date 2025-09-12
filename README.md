# Docker Containers (ITCS 6190/8190)

This project runs a **two-container stack** with:
- **PostgreSQL** database seeded with trip data.
- **A Python app** that connects to Postgres, queries the data, computes statistics, and outputs results to both stdout and a JSON file.

---

## 📂 Repository Layout
```
.
├─ app/
│  ├─ Dockerfile      # Python app container
│  └─ main.py         # Application code
├─ db/
│  ├─ Dockerfile      # Postgres container
│  └─ init.sql        # Schema + seed data
├─ out/               # Host folder where summary.json is written
├─ compose.yml        # Defines both services
└─ run.sh             # Bash script to build and run the stack
```

---

## ⚙️ Prerequisites
- Docker Desktop (Linux containers enabled)
- Docker Compose v2 (bundled with Docker Desktop)
- Bash shell (to run `run.sh`)

---

## 🚀 Quick Start
From the repository root:

```bash
# build and run both services
bash run.sh
```

This will:
1. Build the Postgres + Python images  
2. Start Postgres, wait until healthy  
3. Run the Python app to compute stats  
4. Print summary to console  
5. Write results to `./out/summary.json`  

To stop and remove everything:

```bash
docker compose down -v
```

To reset the `out/` folder:

```bash
rm -rf ./out && mkdir -p ./out
```

---

## 📊 Example Output

### Stdout
```
=== Summary ===
{
  "total_trips": 6,
  "avg_fare_by_city": [
    { "city": "Charlotte", "avg_fare": 16.25 },
    { "city": "New York", "avg_fare": 19.0 },
    { "city": "San Francisco", "avg_fare": 20.25 }
  ],
  "top_by_minutes": [
    { "id": 6, "city": "San Francisco", "minutes": 28, "fare": 29.3 },
    { "id": 4, "city": "New York", "minutes": 26, "fare": 27.1 },
    { "id": 2, "city": "Charlotte", "minutes": 21, "fare": 20.0 },
    { "id": 1, "city": "Charlotte", "minutes": 12, "fare": 12.5 },
    { "id": 5, "city": "San Francisco", "minutes": 11, "fare": 11.2 },
    { "id": 3, "city": "New York", "minutes": 9, "fare": 10.9 }
  ]
}
```

### File `out/summary.json`
```json
{
  "total_trips": 6,
  "avg_fare_by_city": [
    { "city": "Charlotte", "avg_fare": 16.25 },
    { "city": "New York", "avg_fare": 19.0 },
    { "city": "San Francisco", "avg_fare": 20.25 }
  ],
  "top_by_minutes": [
    { "id": 6, "city": "San Francisco", "minutes": 28, "fare": 29.3 },
    { "id": 4, "city": "New York", "minutes": 26, "fare": 27.1 },
    { "id": 2, "city": "Charlotte", "minutes": 21, "fare": 20.0 },
    { "id": 1, "city": "Charlotte", "minutes": 12, "fare": 12.5 },
    { "id": 5, "city": "San Francisco", "minutes": 11, "fare": 11.2 },
    { "id": 3, "city": "New York", "minutes": 9, "fare": 10.9 }
  ]
}
```

---

## 🛠️ Troubleshooting
- **Docker engine not running** → Open Docker Desktop and wait for “Engine running.”
- **Port 5432 already in use** → Stop other Postgres instances, or map to a different port in `compose.yml`.
- **App exits before DB is ready** → This stack uses a healthcheck; if running services manually, start DB first.
- **Permission errors writing to `out/`** → Ensure the folder exists and you have write access. Recreate with:
  ```bash
  rm -rf ./out && mkdir -p ./out
  ```

---


