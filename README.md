# Docker Containers (ITCS 6190/8190)

This project runs a **two-container stack** with:
- **PostgreSQL** database seeded with trip data.
- **Lightweight Python app** that connects to Postgres, queries the data, computes simple statistics, and outputs results to both stdout and a JSON file.

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
└─ Makefile           # Optional (if GNU Make is installed)
```

---

## ⚙️ Prerequisites
- Docker Desktop (Linux containers enabled)
- Docker Compose v2 (bundled with Docker Desktop)
- (Optional) GNU Make if you want to use the Makefile commands

---

## 🚀 Quick Start (without Make)
From the repository root:

```powershell
# build and run both services
docker compose up --build
```

This will:
1. Build the Postgres + Python images  
2. Start Postgres, wait until healthy  
3. Run the Python app to compute stats  
4. Print summary to console  
5. Write results to `./out/summary.json`  

To stop and remove everything:

```powershell
docker compose down -v
```

To reset the `out/` folder in PowerShell:

```powershell
Remove-Item -Recurse -Force .\out
New-Item -ItemType Directory -Path .\out | Out-Null
```

---

## 🖥️ One-Command Run (with Make)
If you have `make` installed:

```powershell
make all
```

This will clean the `out/` folder, rebuild images, run the stack, and produce the summary.

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
- **PowerShell vs bash commands** → PowerShell does not support `rm -rf`; use `Remove-Item` instead (see above).
- **App exits before DB is ready** → This stack uses a healthcheck; if running services manually, start DB first.
- **Permission errors writing to `out/`** → Ensure the folder exists and you have write access. Recreate with:
  ```powershell
  Remove-Item -Recurse -Force .\out
  New-Item -ItemType Directory -Path .\out | Out-Null
  ```

---

## 📝 Exact Commands I Used
```powershell
# verify docker
docker --version
docker compose version

# build images
docker build -t trips-db:dev db
docker build -t trips-app:dev app

# run stack
docker compose up --build

# check output file
Get-Content .\out\summary.json

# stop and clean
docker compose down -v
Remove-Item -Recurse -Force .\out
New-Item -ItemType Directory -Path .\out | Out-Null
```

---
