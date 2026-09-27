from pathlib import Path
import tempfile
import threading

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from pyinit.generator import generate_project, generate_project_zip
from pyinit.runner import (
    create_venv,
    venv_python_path,
    install_project,
    find_free_port,
    launch_fastapi_background,
)


app = FastAPI(title="pyinit_web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
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


# Tracks the one currently-running "Generate & Run" preview server, if any.
_current_process = None
_current_timer = None
_RUN_TIMEOUT_SECONDS = 300  # auto-stop after 5 minutes


def _stop_current_run() -> None:
    global _current_process, _current_timer

    if _current_timer is not None:
        _current_timer.cancel()
        _current_timer = None

    if _current_process is not None:
        _current_process.terminate()
        _current_process = None


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


@app.post("/api/generate-and-run")
def generate_and_run(request: GenerateRequest):
    global _current_process, _current_timer

    if request.stack != "fastapi":
        raise HTTPException(
            status_code=400,
            detail="Generate & Run is only available for the FastAPI stack.",
        )

    # Stop whatever preview was already running before starting a new one.
    _stop_current_run()

    output_dir = Path(tempfile.mkdtemp())

    project_dir = generate_project(
        name=request.name,
        stack=request.stack,
        pm=request.pm,
        py=request.py,
        ci=request.ci,
        docker=request.docker,
        output_dir=output_dir,
    )

    venv_dir = create_venv(project_dir)
    venv_python = venv_python_path(venv_dir)
    install_project(project_dir, venv_python)

    port = find_free_port()
    package_name = request.name.replace("-", "_")

    _current_process = launch_fastapi_background(project_dir, venv_python, package_name, port)
    _current_timer = threading.Timer(_RUN_TIMEOUT_SECONDS, _stop_current_run)
    _current_timer.daemon = True
    _current_timer.start()

    return {"docs_url": f"http://127.0.0.1:{port}/docs"}