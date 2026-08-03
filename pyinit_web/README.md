# PyInit Backend

This directory contains the FastAPI backend for PyInit. It exposes the REST API used by the web interface and the CLI to generate Python projects.

## Requirements

- Python 3.10+
- Poetry

## Installation

```bash
poetry install
```

## Run

```bash
poetry run uvicorn pyinit_web.main:app --reload
```

The backend runs on:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

## Tests

```bash
pytest
```