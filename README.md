# Automated Video Analysis Tool for Quantifying Bulbar Function

This repository processes patient videos and estimates tongue sweep frequency for bulbar-function analysis.

The core processing flow is unchanged:
1. Optional video stabilization
2. Optional compression
3. Optional face extraction
4. Optional lip extraction
5. Tongue movement frequency estimation (with optional Excel output)

## What Was Added for Production Readiness

- Import/path hardening so the app can be launched from repo root reliably.
- Model-path resolution with sensible defaults (`model_weights/final_model.h5` first).
- Fixed broken `callPerformAll` argument forwarding in pipeline orchestration.
- Added a basic web UI (`Streamlit`) to run the pipeline.
- Added CLI entrypoint (`run_pipeline.py`) for non-GUI execution.
- Added unit tests for orchestration behavior with mocking.
- Added `requirements.txt`, `Dockerfile`, and `.dockerignore`.

## Repository Layout

```text
.
├── Codes/
│   ├── Pipeline.py
│   ├── Pipeline_executer.py
│   ├── GUI.py
│   ├── basic_ui.py
│   └── src/
├── model_weights/
│   └── final_model.h5
├── run_pipeline.py
├── requirements.txt
├── Dockerfile
└── tests/
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

### 1. Existing Desktop GUI (PySimpleGUI)

```bash
python Codes/Pipeline_executer.py
```

### 2. Basic Web UI (Streamlit)

```bash
streamlit run Codes/basic_ui.py
```

### 3. CLI Runner

Example:

```bash
python run_pipeline.py \
  --input /absolute/path/to/video.mov \
  --face-extract \
  --lip-extract \
  --frequency \
  --save-in-excel
```

You can also add `--stabilize`, `--compress`, and parameter overrides (`--threshold`, `--time-slice`, etc.).

## Running Tests

```bash
pytest -q
```

Current tests focus on orchestration correctness:
- Stage ordering
- Input artifact selection priority
- Excel update invocation
- `callPerformAll` forwarding correctness

## Docker

Build:

```bash
docker build -t bulbar-analysis:local .
```

Run web UI:

```bash
docker run --rm -p 8501:8501 -v "$PWD:/app" bulbar-analysis:local
```

Then open `http://localhost:8501`.

## Notes

- The main analysis logic was intentionally preserved.
- The model file is expected at `model_weights/final_model.h5` (or set `BULBAR_MODEL_PATH`).
- `Frequency.xlsx` must exist if Excel export is enabled in pipeline execution.
