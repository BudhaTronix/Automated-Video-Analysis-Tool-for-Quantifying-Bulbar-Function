import argparse
from pathlib import Path

from keras.models import load_model

from Codes.Pipeline import pipeline


def _resolve_model_path(custom_model):
    if custom_model:
        return Path(custom_model).expanduser()

    repo_root = Path(__file__).resolve().parent
    candidates = [
        repo_root / "model_weights" / "final_model.h5",
        repo_root / "Codes" / "final_model.h5",
    ]
    for model_path in candidates:
        if model_path.exists():
            return model_path
    return candidates[0]


def build_parser():
    parser = argparse.ArgumentParser(description="Run the bulbar analysis pipeline.")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--model", default="", help="Model path (.h5)")
    parser.add_argument("--stabilize", action="store_true", help="Run stabilization")
    parser.add_argument("--compress", action="store_true", help="Run compression")
    parser.add_argument("--face-extract", action="store_true", help="Run face extraction")
    parser.add_argument("--lip-extract", action="store_true", help="Run lip extraction")
    parser.add_argument("--frequency", action="store_true", help="Run frequency analysis")
    parser.add_argument("--threshold", type=int, default=40)
    parser.add_argument("--thresh-iterations", type=int, default=2)
    parser.add_argument("--visual-area", type=int, default=0)
    parser.add_argument("--disp", action="store_true", help="Show frame-level debug plots")
    parser.add_argument("--correction-face", type=int, default=30)
    parser.add_argument("--correction-lip", type=int, default=30)
    parser.add_argument("--save-in-excel", action="store_true", help="Write output to Frequency.xlsx")
    parser.add_argument("--time-slice", type=int, default=5)
    parser.add_argument("--smoothing-radius", type=int, default=50)
    return parser


def main():
    args = build_parser().parse_args()
    input_video = Path(args.input).expanduser()
    if not input_video.exists():
        raise FileNotFoundError(f"Input video not found: {input_video}")

    model_path = _resolve_model_path(args.model)
    model = load_model(str(model_path), compile=False)

    runner = pipeline()
    runner.CUI(
        str(input_video),
        args.stabilize,
        args.compress,
        args.face_extract,
        args.lip_extract,
        args.frequency,
        args.threshold,
        args.thresh_iterations,
        args.visual_area,
        args.disp,
        args.correction_face,
        args.correction_lip,
        args.save_in_excel,
        args.time_slice,
        model,
        args.smoothing_radius,
    )


if __name__ == "__main__":
    main()

