# Name Demographics API 🌍

A high-performance, fully decoupled REST API built with FastAPI. This service concurrently aggregates demographic predictions (gender, age, and nationality) based on a given name using external data providers, and securely persists the records to a cloud PostgreSQL database.

## 🚀 Features

* **Concurrent Data Fetching:** Uses `httpx` and `asyncio.gather` to request data from three external APIs simultaneously, reducing latency.
* **Strict Idempotency:** Enforces database-level constraints and custom UUID v7 generation to prevent duplicate entries and handle race conditions.
* **Data Validation:** Leverages Pydantic schemas to strictly validate incoming payloads and sanitize outgoing JSON responses.
* **Resilient Error Handling:** Custom exception handlers intercept external API failures (502s) and invalid client requests, ensuring standardized JSON error contracts.
* **Serverless Deployment:** Fully optimized and configured for Vercel edge deployment using Vercel's Python runtime.

## 🛠 Tech Stack

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL (Supabase)
* **ORM:** SQLAlchemy
* **Data Validation:** Pydantic
* **Async HTTP:** HTTPX
* **Deployment:** Vercel

## 📦 External APIs Integrated
* [Genderize.io](https://genderize.io)
* [Agify.io](https://agify.io)
* [Nationalize.io](https://nationalize.io)

---

## Live url
https://name-demo-roan.vercel.app/

## 💻 Local Development Setup

### 1. Prerequisites
* Python 3.10+
* A [Supabase](https://supabase.com/) account (for the PostgreSQL database)

### 2. Clone and Configure
Clone the repository to your local machine:
```bash
git clone (https://github.com/carl-yom/Name-Demo.git)
cd name_demographics