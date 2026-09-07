# 🚀 Vibeosys Product Management API (FastAPI + MySQL)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg)](https://docs.pydantic.dev/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](https://www.mysql.com/)

A high-performance standalone REST API built using **FastAPI**, **SQLAlchemy ORM**, **Pydantic v2**, and **MySQL** for managing products with full pagination, validation, and auto-documentation.

---

## 📌 Features

- **CRUD Operations**:
  - `GET /product/list` - Paginated product listing with 10 records per page by default.
  - `GET /product/{pid}/info` - Retrieve product details by ID.
  - `POST /product/add` - Add new product with rigorous Pydantic validation.
  - `PUT /product/{pid}/update` - Update product attributes by ID.
- **Database Schema**:
  - `id`: BigInteger, Primary Key, Auto Increment
  - `name`: VARCHAR(100), Not Null
  - `category`: Enum (`finished`, `semi-finished`, `raw`)
  - `description`: VARCHAR(250)
  - `product_image`: TEXT (image URL)
  - `sku`: VARCHAR(100), Indexed
  - `unit_of_measure`: Enum (`mtr`, `mm`, `ltr`, `ml`, `cm`, `mg`, `gm`, `unit`, `pack`)
  - `lead_time`: INT (in days)
  - `created_date`: TIMESTAMP (auto-generated)
  - `updated_date`: TIMESTAMP (auto-updated)
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Automated Test Suite**: Unit & integration tests via `pytest` with 100% endpoint coverage.

---

## 🏗️ Project Architecture

```
vibeosys-fastapi-assignment/
├── app/
│   ├── __init__.py          # Package init
│   ├── main.py              # FastAPI app instance, CORS & lifespan
│   ├── config.py            # Environment & database settings
│   ├── database.py          # SQLAlchemy engine, session & dependency
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py       # SQLAlchemy Product model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── product.py       # Pydantic schemas (requests & responses)
│   ├── crud/
│   │   ├── __init__.py
│   │   └── product.py       # Database operations
│   └── routers/
│       ├── __init__.py
│       └── product.py       # API endpoints (/product/*)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and in-memory test DB
│   └── test_product.py      # Automated tests
├── .env.example             # Environment template
├── .gitignore               # Standard gitignore
├── requirements.txt         # Project dependencies
├── Readme.txt               # Plaintext instructions
└── README.md                # Project documentation
```

---

## ⚡ Quickstart & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<username>/vibeosys-fastapi-assignment.git
cd vibeosys-fastapi-assignment
```

### 2. Set up virtual environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Database (.env)
Create a `.env` file (or copy from `.env.example`):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=vibeosys_db
```

Make sure the database is created in MySQL:
```sql
CREATE DATABASE vibeosys_db;
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload
```

- **API Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) *(or [http://localhost:8000/](http://localhost:8000/))*
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints Reference

### 1. Add Product (`POST /product/add`)
**Request Body**:
```json
{
  "name": "Industrial Electric Motor",
  "category": "finished",
  "description": "High-torque 3-phase AC induction motor",
  "product_image": "https://example.com/images/motor.jpg",
  "sku": "MOT-IND-001",
  "unit_of_measure": "unit",
  "lead_time": 14
}
```

### 2. List Products (`GET /product/list?page=1&limit=10`)
**Response**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Industrial Electric Motor",
      "category": "finished",
      "description": "High-torque 3-phase AC induction motor",
      "product_image": "https://example.com/images/motor.jpg",
      "sku": "MOT-IND-001",
      "unit_of_measure": "unit",
      "lead_time": 14,
      "created_date": "2026-09-07T15:30:00",
      "updated_date": "2026-09-07T15:30:00"
    }
  ],
  "total_records": 1,
  "current_page": 1,
  "page_size": 10,
  "total_pages": 1,
  "has_next": false,
  "has_previous": false
}
```

### 3. Get Product Info (`GET /product/{pid}/info`)
**Response**:
```json
{
  "id": 1,
  "name": "Industrial Electric Motor",
  "category": "finished",
  "description": "High-torque 3-phase AC induction motor",
  "product_image": "https://example.com/images/motor.jpg",
  "sku": "MOT-IND-001",
  "unit_of_measure": "unit",
  "lead_time": 14,
  "created_date": "2026-09-07T15:30:00",
  "updated_date": "2026-09-07T15:30:00"
}
```

### 4. Update Product (`PUT /product/{pid}/update`)
**Request Body**:
```json
{
  "name": "Industrial Electric Motor V2",
  "lead_time": 21
}
```

---

## 🧪 Running Automated Tests

Run the test suite with pytest:
```bash
pytest -v
```
All unit and integration tests run isolated in memory with no external database dependency required.
