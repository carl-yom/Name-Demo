Here’s a **clean, unified README** that merges your original (public-facing API + deployment) with your new (system design + NLP engine). It reads like a serious production backend and keeps your links intact.

---

# Insighta Labs Demographic Intelligence API 🌍

A high-performance, production-grade REST API built with FastAPI for demographic intelligence. This service enables querying, filtering, sorting, and paginating through user profile data, while also supporting a **rule-based Natural Language Query Engine** that translates plain English into structured database filters — without relying on external AI or LLMs.

---

## 🚀 Live API

[https://name-demo-roan.vercel.app/](https://name-demo-roan.vercel.app/)

---

## ✨ Core Features

### ⚡ High-Performance Backend

- Built with **FastAPI** for speed and async support
- Optimized query execution with dynamic filtering, sorting, and pagination
- PostgreSQL-backed persistence via Supabase

### 🧠 Natural Language Query Engine (No AI Required)

- Converts plain English queries into structured database filters
- Fully rule-based (deterministic, fast, and cost-free)
- Zero external AI/LLM dependencies

### ⚙️ Concurrent & Efficient Design

- Async-ready architecture
- O(1) in-memory lookups for country resolution
- Minimal latency during request lifecycle

### 🛡 Robust Data Integrity

- UUID v7 for globally unique, chronologically sortable IDs
- Idempotent database operations
- Graceful handling of duplicate insertions and failures

### 📦 Clean API Contracts

- Strict validation using Pydantic
- Standardized JSON error responses
- Clear separation between request parsing and data access

---

## 🏗 Architectural Design

### 1. Separation of Concerns (Flat Architecture)

The system is intentionally modular and maintainable:

- **`main.py` (Controller Layer)**
  Handles routing, dependency injection, and HTTP-level concerns only.

- **`crud.py` (Data Access Layer)**
  Responsible for all database interactions using SQLAlchemy.
  Uses `getattr()` for safe dynamic sorting and prevents SQL injection.

- **`nlp_parser.py` (Parsing Engine)**
  A pure Python module that tokenizes and maps natural language into filters.
  Completely decoupled from the database.

---

### 2. O(1) In-Memory Country Resolution

- A `countries.json` file stores 195+ countries and aliases mapped to ISO codes
- Loaded into memory at application startup using FastAPI lifespan
- Enables **instant lookup (O(1))** during query parsing

**Why it matters:**
No database calls are needed to resolve country filters → significantly reduced latency.

---

### 3. Graceful Failure & Idempotency

- Invalid queries return structured **400-level errors**
- Database conflicts handled via transaction rollback
- Duplicate-safe operations for repeated executions

---

## 🧠 Natural Language Query Engine

The `/api/profiles/search` endpoint processes queries in two stages:

### Phase 1: Tokenization (`clean_and_split`)

- Converts input to lowercase
- Removes punctuation (`,` `-` `.` `!`)
- Splits into tokens

**Example:**
`"young adult males from naija"`
→ `["young", "adult", "males", "from", "naija"]`

---

### Phase 2: Dictionary Mapping (`extract_filters`)

Each token is matched against predefined mappings:

#### Gender

- male → men, males, boys
- female → women, females, girls

#### Age Groups

- adult, teens, children, seniors

#### Age Ranges

- `"young"` → `min_age=16`, `max_age=24`

#### Countries

- Uses ISO mapping from cache
- Example: `"naija"` → `"NG"`

---

### ✅ Example Execution

**Query:**
`young adult males from naija`

**Parsed Filters:**

```json
{
  "min_age": 16,
  "max_age": 24,
  "age_group": "adult",
  "gender": "male",
  "country_id": "NG"
}
```

---

## ⚠️ Limitations

This system is intentionally rule-based for speed and reliability:

- ❌ No negation handling
  ("not from nigeria" is ignored)

- ❌ No dynamic numeric parsing
  ("above 30", "between 18 and 45")

- ❌ Conflicting keywords overwrite sequentially
  ("young seniors")

- ❌ Severe misspellings not supported
  ("nigreia")

- ⚠️ Multi-word countries require exact or alias matches

---

## 🛠 Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Async HTTP:** HTTPX
- **Deployment:** Vercel

---

## 📦 External APIs (Legacy Data Ingestion)

- [https://genderize.io](https://genderize.io)
- [https://agify.io](https://agify.io)
- [https://nationalize.io](https://nationalize.io)

---

## 💻 Local Development Setup

### 1. Prerequisites

- Python 3.10+
- Supabase account (PostgreSQL database)

---

### 2. Clone Repository

```bash
git clone https://github.com/carl-yom/Name-Demo.git
cd name_demographics
```

---

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

---

### 4. Seed the Database

```bash
python seed.py
```

---

### 5. Run the Server

```bash
uvicorn main:app --reload
```

Visit:

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧭 Design Philosophy

This project prioritizes:

- **Deterministic performance over probabilistic AI**
- **Explicit control over hidden abstraction**
- **Scalable backend patterns for real-world systems**
