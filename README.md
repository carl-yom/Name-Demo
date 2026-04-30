# Insighta Labs+ Intelligence Platform 🌍

A **high-performance, production-grade demographic intelligence platform** built with **FastAPI**, designed to provide secure, role-based access to profile data through a unified REST API consumed by both a **Web Portal** and a **Command Line Interface (CLI)**.

Insighta Labs+ combines:

- Secure GitHub OAuth2 + PKCE authentication
- Role-Based Access Control (RBAC)
- Natural Language Query Parsing (AI-free)
- Dynamic filtering
- HATEOAS pagination
- Structured CSV exports
- Production-ready DevOps practices

---

## 🚀 Live Environments

### Web Portal

[https://insighta-web-nu.vercel.app](https://insighta-web-nu.vercel.app)

### API Base URL

[https://name-demo-roan.vercel.app](https://name-demo-roan.vercel.app)

---

# 🏗 System Architecture

Insighta Labs+ follows a **decoupled three-tier architecture** to maintain scalability, maintainability, and a single source of truth.

## Core Components

### Backend API (FastAPI)

The central intelligence engine responsible for:

- Business logic
- Authentication
- Role enforcement
- NLP query parsing
- Data persistence
- Token issuance
- Rate limiting

### Web Portal (Vanilla JS / SPA)

A browser-based dashboard for:

- Searching profiles
- Viewing analytics
- Admin management
- Secure browser authentication

### CLI Tool (Python)

A globally installable terminal interface for:

- Developer workflows
- Power-user automation
- Secure local authentication
- Data export

---

# 🧱 Design Philosophy

## Flat Architecture

Strict separation of concerns:

- `main.py` → Controllers / Routing
- `crud.py` → Data Access Layer
- `security.py` → Auth / RBAC
- `nlp_parser.py` → Business Logic

---

## O(1) In-Memory Lookups

Country aliases and NLP mappings are loaded into memory during application lifespan startup, enabling:

- Zero database latency for NLP country resolution
- Faster search performance
- Predictable query execution

---

## Graceful Failure & Idempotency

- Transaction rollback on conflicts
- Duplicate-safe writes
- Stable API behavior under repeated requests

---

# 🔐 Authentication & Token Handling Flow

Insighta Labs+ uses **GitHub OAuth2.0 + PKCE (Proof Key for Code Exchange)** for secure user identity verification.

---

## Token Lifecycle

### Access Token

- JWT
- Expires in **3 minutes**

### Refresh Token

- JWT
- Expires in **5 minutes**

---

## Token Rotation

Calling:

```bash
/auth/refresh
```

Immediately:

- Invalidates old refresh token
- Issues new access token
- Issues new refresh token

---

# Interface-Specific Token Delivery

## 🌐 Web Portal

Tokens are delivered via:

- HTTP-Only Cookies
- Secure Cookies
- SameSite=None

### Security Benefits:

- Prevents JavaScript token theft
- Protects against XSS
- Browser-native session handling

---

## 💻 CLI Tool

Tokens are delivered as:

```json id="g0j4h8"
{
  "access_token": "...",
  "refresh_token": "..."
}
```

Stored securely at:

```bash
~/.insighta/credentials.json
```

### CLI Security Flow:

- Localhost callback server
- PKCE verifier
- Manual Bearer token transport

---

# 🛡 Role Enforcement Logic (RBAC)

Access control is enforced through FastAPI Dependency Injection.

---

## Analyst (Default)

### Permissions:

- List profiles
- Search profiles
- View profiles
- Export CSV

---

## Admin

### Additional Permissions:

- Create profiles
- Delete profiles
- Full platform management

---

## Suspension Logic

Users with:

```python id="9fwjuz"
is_active = False
```

Are globally blocked from all authenticated access.

---

# 🧠 Natural Language Parsing Engine (AI-Free)

The `/api/profiles/search` endpoint transforms plain English into structured SQL-ready filters without external AI or LLMs.

---

# Parsing Pipeline

## Phase 1: Tokenization (`clean_and_split`)

Example:

```txt id="j8zv6p"
"young adult males from naija"
```

Becomes:

```python id="yec6pn"
["young", "adult", "males", "from", "naija"]
```

---

## Phase 2: Rule-Based Extraction (`extract_filters`)

### Gender:

```txt id="eyv5oc"
male → men, males, boys
```

### Age:

```txt id="u5m8i9"
young → min_age=16, max_age=24
```

### Country:

```txt id="v6r3nz"
naija → NG
```

---

## Output:

```json id="amc2zd"
{
  "min_age": 16,
  "max_age": 24,
  "age_group": "adult",
  "gender": "male",
  "country_id": "NG"
}
```

---

# ⚙️ Core API Features

## API Version Enforcement

All `/api/*` endpoints require:

```http id="7g3c4v"
X-API-Version: 1
```

Missing header:

```txt id="pkm7p2"
400 Bad Request
```

---

## HATEOAS Pagination

Every paginated response includes:

- `page`
- `total`
- `total_pages`
- `self`
- `next`
- `prev`

---

## CSV Export

Endpoint:

```bash
/api/profiles/export
```

Supports:

- Full filtering
- Large dataset streaming
- Structured downloads

---

# 🚦 Rate Limiting

## Authentication Endpoints:

```txt id="dbsqgk"
/auth/* → 10 requests/minute
```

---

## Standard API:

```txt id="7nryaw"
/api/* → 60 requests/minute
```

---

# 💻 CLI Usage

## Installation

```bash
pip install insighta-cli
```

---

# Authentication Commands

```bash
insighta login
insighta whoami
insighta logout
```

---

# Profile Commands

## List Profiles

```bash
insighta profiles list
```

---

## Filtered Queries

```bash
insighta profiles list --country NG --age-group adult --gender male
insighta profiles list --min-age 25 --max-age 40
insighta profiles list --sort-by age --order desc --page 2 --limit 20
```

---

## Natural Language Search

```bash
insighta profiles search "young males from nigeria"
```

---

## Admin Operations

```bash
insighta profiles create --name "Harriet Tubman"
insighta profiles get <id>
```

---

## CSV Export

```bash
insighta profiles export --format csv --gender male --country NG
```

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python 3.10+
- SQLAlchemy ORM
- Pydantic

---

## Database

- PostgreSQL
- Supabase

---

## Frontend

- Vanilla JavaScript SPA

---

## Authentication

- GitHub OAuth2
- PKCE
- JWT

---

## DevOps

- GitHub Actions
- Linting
- Automated tests
- Conventional Commits
- Branch Protection

---

## Deployment

- Vercel Serverless Functions

---

# 💻 Local Development Setup

# 1. Prerequisites

- Python 3.10+
- Supabase PostgreSQL
- GitHub OAuth App

---

# 2. Clone Repository

```bash
git clone https://github.com/carl-yom/Name-Demo.git
cd name_demographics
pip install -r requirements.txt
```

---

# 3. Environment Variables (`.env`)

```env
WEB_GITHUB_CLIENT_ID=your_web_id
WEB_GITHUB_CLIENT_SECRET=your_web_secret
WEB_GITHUB_REDIRECT_URI=http://localhost:8000/auth/web/callback

JWT_SECRET_KEY=your_secure_secret
ALGORITHM=HS256
```

---

# 4. Run Development Server

```bash
uvicorn main:app --reload
```

---

## Local API:

```txt id="s9v3wn"
http://127.0.0.1:8000
```

---

## Swagger Docs:

```txt id="4tkbpt"
/docs
```

---

# 🎯 Engineering Highlights

## Built for:

- Security
- Scalability
- Maintainability
- Multi-client architecture
- AI-free deterministic NLP
- Production deployment

---

# 📌 Project Standard

Insighta Labs+ is designed not as a simple CRUD API, but as a **product-grade intelligence platform** demonstrating:

- Full-stack system design
- Product engineering
- Security architecture
- Developer tooling
- Real-world deployment practices.
