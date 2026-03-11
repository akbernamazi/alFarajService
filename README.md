# Aza API Service

FastAPI service exposing versioned REST APIs for web and mobile clients.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Base URL: `http://localhost:4000`

## Routes

- `GET /health`
- `GET /api/v1/health`
- `GET /api/v1/events/public`
- `GET /api/v1/events/private?userId=u1`
- `GET /api/v1/events/{event_id}`
- `POST /api/v1/events`
- `POST /api/v1/events/{event_id}/invite`
- `GET /api/v1/prayer-times?date=YYYY-MM-DD&lat=&lng=`
- `GET /api/v1/prayer-places`
