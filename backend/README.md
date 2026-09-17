# Honey Chain API

Prototype FastAPI service for hive telemetry and honey batch traceability.

## Start

```bash
cd backend
python -m venv .venv
# activate the virtual environment
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `/docs` for the interactive OpenAPI interface.

## Main endpoints

- `GET /health`
- `POST /api/v1/telemetry` — ingest hive temperature, humidity and weight; returns baseline AI health analysis and a payload hash.
- `GET /api/v1/hives` — latest readings.
- `POST /api/v1/batches` — create traceable honey batch.
- `GET /api/v1/batches/{batch_id}` — consumer/batch verification.
- `POST /api/v1/batches/{batch_id}/events?event=...` — append a controlled supply-chain event.

## Production notes

This prototype keeps state in memory and hashes records locally. Production should use PostgreSQL, authenticated role-based APIs, an append-only audit/event table, signed IoT payloads, MQTT ingestion, secrets management and an actual blockchain adapter. Do not interpret the baseline rule-based health score as a medical/veterinary diagnosis; alerts should trigger beekeeper/expert inspection and validated models should be developed from representative field data.
