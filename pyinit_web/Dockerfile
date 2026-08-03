# syntax=docker/dockerfile:1
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install -e .
EXPOSE 8000
CMD ["uvicorn", "pyinit_web.main:app", "--host", "0.0.0.0", "--port", "8000"]