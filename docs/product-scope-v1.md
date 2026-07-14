# CardIntel v1.0 scope

## Must have

- Authentication: registration, login, JWT bearer tokens, and role-based admin access.
- Card discovery: search by card or bank and filters for LTF, cashback, fuel, movies, lounge, travel, UPI, forex, reward type, network, annual/joining fees, salary, occupation, student, and self-employed eligibility.
- Recommendations based on salary, occupation, monthly spends, interested categories, preferred banks, and LTF preference. Results include top cards, rationale, pros, cons, and policy date.
- Card profiles: fees, waiver, eligibility, benefits, reward rates and caps, redemption, hidden charges, exclusions, policy date, and official source.
- Admin: banks and cards, manual sync trigger, sync logs, weekly policy sync, policy version history, and old-to-new policy comparisons.
- Comparison of two to four cards.

## Deferred

v1.1: reward simulator, personalized dashboard, bookmarks, recently viewed, and recommendation history.

Future: AI chat, Reddit summaries, browser extension, mobile app, and offer alerts.

## Architecture decisions

- FastAPI modular monolith with SQLAlchemy 2, Alembic, Pydantic v2, PostgreSQL, and Celery/Redis.
- React 19 + TypeScript + Vite with MUI, React Router, Axios, and TanStack Query.
- PostgreSQL full-text search first; OpenSearch only after a measured need.
- Parsing uses Requests, BeautifulSoup4, PyMuPDF, and pdfplumber; Playwright only for JavaScript-only sources.
- AI extraction is optional and is not part of the MVP path.
