# PyInit UI

This directory contains the React + Vite frontend for PyInit. It provides the user interface for configuring and generating Python projects through the FastAPI backend.

## Requirements

- Node.js 18+
- npm

## Installation

```bash
npm install
```

## Run

```bash
npm run dev
```

The application runs at:

```
http://localhost:5173
```

## Build

```bash
npm run build
```

## Backend

The frontend expects the PyInit backend to be running.

Start the backend from the `pyinit_web` directory:

```bash
poetry run uvicorn pyinit_web.main:app --reload
```