from pathlib import Path
import tempfile

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from pyinit.generator import generate_project_zip


app = FastAPI(title="pyinit_web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    name: str
    stack: str = "fastapi"
    pm: str = "poetry"
    py: str = "3.9"
    ci: str = "github"
    docker: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate")
def generate(request: GenerateRequest):
    temp_dir = Path(tempfile.mkdtemp())

    zip_path = generate_project_zip(
        name=request.name,
        stack=request.stack,
        pm=request.pm,
        py=request.py,
        ci=request.ci,
        docker=request.docker,
        output_dir=temp_dir,
    )

    return FileResponse(
        path=zip_path,
        filename=f"{request.name}.zip",
        media_type="application/zip",
    )