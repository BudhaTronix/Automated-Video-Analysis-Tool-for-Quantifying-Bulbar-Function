import sys
import importlib.util
from pathlib import Path

import streamlit as st

try:
    from keras.models import load_model
except ImportError:
    from tensorflow.keras.models import load_model

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))


def _load_pipeline_class():
    try:
        from Codes.Pipeline import pipeline as pipeline_cls
        return pipeline_cls
    except ModuleNotFoundError as exc:
        if exc.name not in {"Codes", "Codes.Pipeline"}:
            raise

    try:
        from Pipeline import pipeline as pipeline_cls
        return pipeline_cls
    except ModuleNotFoundError as exc:
        if exc.name != "Pipeline":
            raise

    spec = importlib.util.spec_from_file_location("Pipeline", CODE_DIR / "Pipeline.py")
    if spec is None or spec.loader is None:
        raise ImportError("Unable to load Pipeline.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pipeline


pipeline = _load_pipeline_class()


def _resolve_model_path():
    repo_root = Path(__file__).resolve().parent.parent
    candidates = [
        repo_root / "model_weights" / "final_model.h5",
        Path(__file__).resolve().parent / "final_model.h5",
    ]
    for model_path in candidates:
        if model_path.exists():
            return model_path
    return candidates[0]


@st.cache_resource
def _load_model(model_path):
    return load_model(str(model_path), compile=False)


def main():
    st.set_page_config(page_title="Bulbar Video Analysis", layout="centered")
    st.title("Bulbar Video Analysis")
    st.caption("Basic runner for the existing processing pipeline.")

    default_model_path = _resolve_model_path()
    model_path = st.text_input("Model path", value=str(default_model_path))
    input_video = st.text_input("Input video path (.mov/.mp4)", value="")

    col1, col2 = st.columns(2)
    with col1:
        stabilize = st.checkbox("Stabilize", value=False)
        compress = st.checkbox("Compress", value=False)
        face_extract = st.checkbox("Face extraction", value=True)
    with col2:
        lip_extract = st.checkbox("Lip extraction", value=True)
        frequency = st.checkbox("Frequency analysis", value=True)
        save_excel = st.checkbox("Save in Excel", value=True)

    smoothing_radius = st.number_input("Smoothing radius", min_value=1, max_value=200, value=50, step=1)
    visual_area = st.number_input("Visual area correction", min_value=0, max_value=200, value=0, step=1)
    correction_face = st.number_input("Face correction factor", min_value=0, max_value=100, value=30, step=1)
    correction_lip = st.number_input("Lip correction factor", min_value=0, max_value=100, value=30, step=1)
    threshold = st.number_input("Threshold", min_value=1, max_value=255, value=40, step=1)
    thresh_iterations = st.number_input("Threshold iterations", min_value=0, max_value=20, value=2, step=1)
    time_slice = st.number_input("Time slice (seconds)", min_value=1, max_value=120, value=5, step=1)
    disp = st.checkbox("Verbose frame display", value=False)

    if st.button("Run Pipeline"):
        if not input_video:
            st.error("Provide an input video path.")
            return

        input_path = Path(input_video).expanduser()
        if not input_path.exists():
            st.error(f"Input video not found: {input_path}")
            return

        model = _load_model(Path(model_path))
        runner = pipeline()

        with st.spinner("Processing video..."):
            runner.CUI(
                str(input_path),
                stabilize,
                compress,
                face_extract,
                lip_extract,
                frequency,
                int(threshold),
                int(thresh_iterations),
                int(visual_area),
                disp,
                int(correction_face),
                int(correction_lip),
                save_excel,
                int(time_slice),
                model,
                int(smoothing_radius),
            )

        st.success("Pipeline execution completed.")


if __name__ == "__main__":
    main()
