# Parts Unlimited API

## Overview

Parts Unlimited API is a FastAPI application designed to manage parts information. It includes CRUD operations for parts and an endpoint to retrieve the 5 most common words in part descriptions.

## Features

- **CRUD Operations**: Create, read, update, and delete parts.
- **Most Common Words**: Retrieve the 5 most common words in part descriptions.
- **Detailed API Documentation**: Interactive API documentation available at `/docs`.

## Requirements

- Python 3.10
- pip (Python package installer)
- SQLite

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/your-username/parts-unlimited-api.git
cd parts-unlimited-api
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment using the following commands:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```
- **Nota:**  To run test and development purposes use test-requirements.txt instead.

### Environment Configuration

Create a `.env` file in the root directory of the project with the following content:

```env
DATABASE_URL=sqlite:///./app.db
DEBUG=True
```

For testing, create a `.test.env` file:

```env
DATABASE_URL=sqlite:///./test.db
DEBUG=True
```

### Database Migration

Use Alembic for database migrations. Ensure you have configured `alembic.ini` properly.

to create the migration file use:
```bash
alembic revision --autogenerate -m "Initial migration"
```
after that use:

```bash
alembic upgrade head
```

to create the DB and tables

### Run the Application

To start the FastAPI server, use:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Documentation

Interactive API documentation is available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Running Tests

To run the tests, use the following command:

```bash
pytest
```
