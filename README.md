## Databases: SQLite (Flask) and MongoDB (Node)

This project includes a Flask backend (SQLAlchemy) using SQLite by default and a Node/Express backend using MongoDB with Mongoose.

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional, to run MongoDB locally)

### Environment
Copy `.env.example` to `.env` and adjust values. You can place `.env` either in the repository root or in the `backend/` directory.

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL` (Flask/SQLAlchemy) — defaults to SQLite at `backend/procurement.db`
- `MONGODB_URI` (Node/Mongoose) — e.g. `mongodb://localhost:27017/procurement`

---

### SQLite (Flask) Setup
1. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create the database (auto-creates in dev/testing):
   - Ensure `FLASK_CONFIG=development` (default). On first run, tables are created.
   - Alternatively, use migrations:
     ```bash
     export FLASK_APP=run.py
     flask db init
     flask db migrate -m "init"
     flask db upgrade
     ```
3. Run the Flask API:
   ```bash
   python run.py
   ```

The Flask API listens on port 5000.

---

### MongoDB (Node) Setup
Run MongoDB via Docker or your local installation.

Option A: Docker
```bash
docker compose up -d mongo
```

Option B: Local install
- Install MongoDB Community Server and start it locally on port 27017.

Install Node dependencies and start the server:
```bash
cd backend
npm install
npm run start
```

The Node API listens on port 4000 and mounts routes under `/api/workflow`.

---

### Useful Environment Variables
- `FLASK_CONFIG`: `development` | `production` | `testing`
- `DATABASE_URL`: e.g. `sqlite:////absolute/path/to/procurement.db` or a Postgres URL
- `MONGODB_URI`: e.g. `mongodb://localhost:27017/procurement`

---

### Project Layout
- Flask app: `backend/app` (models in `backend/app/models`) — SQLite/SQLAlchemy
- Node app: `backend/server.js`, `backend/routes/workflow.js`, `backend/models/Request.js` — MongoDB/Mongoose

