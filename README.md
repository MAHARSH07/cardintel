# cardintel

`cardintel` is an Indian credit-card discovery and recommendation platform. It is organized as a modular monolith with independently deployable frontend and backend applications.

## Structure

```text
cardintel/
├── frontend/    # Client application
└── backend/     # Server application
```

Each application owns its dependencies, configuration, and documentation.

## Getting started

1. Copy `backend/.env.example` to `backend/.env` and provide a PostgreSQL URL and secure JWT secret.
2. Start the backend from `backend`: `uvicorn app.main:app --reload`.
3. Start the frontend from `frontend`: `npm install` then `npm run dev`.

The agreed v1.0 scope and architecture are recorded in [docs/product-scope-v1.md](docs/product-scope-v1.md).
