================================================================================
           VIBEOSYS FASTAPI PRODUCT MANAGEMENT ASSIGNMENT
================================================================================

A high-performance standalone REST API built using Python 3.11+, FastAPI, 
SQLAlchemy ORM, Pydantic, and MySQL backend database.

--------------------------------------------------------------------------------
TABLE OF CONTENTS
--------------------------------------------------------------------------------
1. Prerequisites
2. Project Structure
3. Installation & Setup
4. Database Configuration (MySQL)
5. Running the Application
6. API Endpoints & Usage
7. Running Automated Tests
8. Git Version Control Instructions

--------------------------------------------------------------------------------
1. PREREQUISITES
--------------------------------------------------------------------------------
- Python 3.11 or higher (Python 3.13 recommended)
- MySQL Server 8.0+ (or MariaDB) installed and running locally
- Git installed on your system

--------------------------------------------------------------------------------
2. PROJECT STRUCTURE
--------------------------------------------------------------------------------
vibeosys-fastapi-assignment/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app, CORS, lifespan startup & routing
│   ├── config.py            # Environment settings & DB connection string
│   ├── database.py          # SQLAlchemy engine, session maker & get_db dependency
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py       # SQLAlchemy Product model (table definition)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── product.py       # Pydantic schemas (validations & serialization)
│   ├── crud/
│   │   ├── __init__.py
│   │   └── product.py       # Database CRUD operations
│   └── routers/
│       ├── __init__.py
│       └── product.py       # Product endpoints (list, info, add, update)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures & isolated in-memory DB setup
│   └── test_product.py      # Automated test suite
├── .env                     # Local environment variables
├── .env.example             # Example environment template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Project dependencies
├── README.md                # Markdown documentation
└── Readme.txt               # Plaintext instructions file

--------------------------------------------------------------------------------
3. INSTALLATION & SETUP
--------------------------------------------------------------------------------
Follow these steps in your terminal:

Step 1: Open terminal in project root directory
    cd vibeosys-fastapi-assignment

Step 2: Create a virtual environment
    On Windows (PowerShell / CMD):
        python -m venv .venv
        .\.venv\Scripts\activate

    On Linux / macOS:
        python3 -m venv .venv
        source .venv/bin/activate

Step 3: Upgrade pip and install all required dependencies
    pip install --upgrade pip
    pip install -r requirements.txt

--------------------------------------------------------------------------------
4. DATABASE CONFIGURATION (MySQL)
--------------------------------------------------------------------------------
Step 1: Start your MySQL service (via XAMPP, MySQL Workbench, or Command Line).

Step 2: Create the database in MySQL:
    CREATE DATABASE vibeosys_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Step 3: Configure `.env` file in the project root:
    Copy `.env.example` to `.env` and fill in your MySQL credentials:

    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_NAME=vibeosys_db

    (Note: On application startup, FastAPI will automatically create the 
    `products` table if it does not already exist.)

--------------------------------------------------------------------------------
5. RUNNING THE APPLICATION
--------------------------------------------------------------------------------
Run the development server with Uvicorn:

    uvicorn app.main:app --reload

Once started, access:
- Root Service Status: http://127.0.0.1:8000/ (or http://localhost:8000/)
- Interactive Swagger UI Docs: http://127.0.0.1:8000/docs
- Alternative ReDoc Docs: http://127.0.0.1:8000/redoc

--------------------------------------------------------------------------------
6. API ENDPOINTS & USAGE
--------------------------------------------------------------------------------

1. LIST PRODUCTS (Pagination: 10 records per page)
   - Method: GET
   - URL: http://localhost:8000/product/list?page=1&limit=10
   - Query Parameters:
       * page: integer (default: 1)
       * limit: integer (default: 10)
   - Response: Returns paginated product list with total_records, total_pages, 
     current_page, page_size, has_next, and items list.

2. GET PRODUCT INFO
   - Method: GET
   - URL: http://localhost:8000/product/{pid}/info
   - Path Parameter:
       * pid: integer (Product ID)
   - Response: Returns detailed info of the requested product or 404 if not found.

3. ADD PRODUCT
   - Method: POST
   - URL: http://localhost:8000/product/add
   - Request Body (JSON):
     {
       "name": "Industrial Electric Motor",
       "category": "finished",
       "description": "High-torque 3-phase AC induction motor",
       "product_image": "https://example.com/images/motor.jpg",
       "sku": "MOT-IND-001",
       "unit_of_measure": "unit",
       "lead_time": 14
     }
   - Allowed Categories: "finished", "semi-finished", "raw"
   - Allowed Units of Measure: "mtr", "mm", "ltr", "ml", "cm", "mg", "gm", "unit", "pack"
   - Status Code: 201 Created

4. UPDATE PRODUCT
   - Method: PUT
   - URL: http://localhost:8000/product/{pid}/update
   - Request Body (JSON):
     {
       "name": "Industrial Electric Motor V2",
       "lead_time": 21
     }
   - Status Code: 200 OK

--------------------------------------------------------------------------------
7. RUNNING AUTOMATED TESTS
--------------------------------------------------------------------------------
The project includes automated tests using pytest and an in-memory SQLite database,
so tests can run anywhere with zero external dependencies:

    pytest -v

All test cases covering creation, all categories/UOMs, validation errors,
404 not found handling, and 10-record pagination will execute and verify automatically.

--------------------------------------------------------------------------------
8. GIT VERSION CONTROL INSTRUCTIONS
--------------------------------------------------------------------------------
To push this code to your GitHub/GitLab account:

1. Initialize git repository:
    git init
    git add .
    git commit -m "Initial commit: Vibeosys FastAPI Product Management Assignment"

2. Create a new repository on GitHub (e.g. github.com/<username>/vibeosys-fastapi-assignment)

3. Link and push to GitHub:
    git branch -M main
    git remote add origin https://github.com/<username>/vibeosys-fastapi-assignment.git
    git push -u origin main

================================================================================
