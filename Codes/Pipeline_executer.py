import glob
import os
from pathlib import Path

from keras.models import load_model

try:
    from Codes.Pipeline import pipeline
except ImportError:
    from Pipeline import pipeline


def _resolve_model_path():
    env_path = os.getenv("BULBAR_MODEL_PATH")
    if env_path:
        return env_path

    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parent
    candidates = [
        repo_root / "model_weights" / "final_model.h5",
        base_dir / "final_model.h5",
        Path("final_model.h5"),
    ]
    for model_path in candidates:
        if model_path.exists():
            return str(model_path)
    return str(candidates[0])


class pipelineExecutor:
    def __init__(self):
        self.model = load_model(_resolve_model_path(), compile=False)
        # Global Variable Declaration
        self.use_GUI = True
        self.SMOOTHING_RADIUS = 50
        self.visual_area = 0
        self.correctionFactor_Face = 30
        self.correctionFactor_Lip = 30
        self.threshold = 40
        self.thresh_iterations = 2
        self.disp = False
        self.save_in_excel = True
        self.time_slice = 5
        # Change Base File Name
        self.MainFile = "37a.mov"
        # Change to Stabilize
        self.Stabilize = False
        # Change it to True if you want Video to be compressed
        self.Video_Compression = False
        # Change it to True if you want Face Extraction
        self.Face_Extract = True
        # Change it to True if you want Tongue Extraction
        self.Lip_Extraction = True
        # Change it to True if you want to calculate the frequency
        self.Frquency_Calculation = True
        # Change it to True if you want to run on All files
        self.Multi_mode = True

    def main(self):
        if self.use_GUI:
            try:
                from Codes.GUI import GUI
            except ImportError:
                from GUI import GUI
            obj = GUI(self.model)
            obj.loaderFunc()
            return

        obj = pipeline()
        if self.Multi_mode:
            for file_name in sorted(glob.iglob("*.mov")):
                print("\n ################################################################# \n")
                print("Working on File Name : ", file_name)
                print("Processing Starts")
                obj.CUI(
                    file_name,
                    self.Stabilize,
                    self.Video_Compression,
                    self.Face_Extract,
                    self.Lip_Extraction,
                    self.Frquency_Calculation,
                    self.threshold,
                    self.thresh_iterations,
                    self.visual_area,
                    self.disp,
                    self.correctionFactor_Face,
                    self.correctionFactor_Lip,
                    self.save_in_excel,
                    self.time_slice,
                    self.model,
                    self.SMOOTHING_RADIUS,
                )
                print("Processing Ends")
                print("\n ################################################################# \n")
            return

        obj.CUI(
            self.MainFile,
            self.Stabilize,
            self.Video_Compression,
            self.Face_Extract,
            self.Lip_Extraction,
            self.Frquency_Calculation,
            self.threshold,
            self.thresh_iterations,
            self.visual_area,
            self.disp,
            self.correctionFactor_Face,
            self.correctionFactor_Lip,
            self.save_in_excel,
            self.time_slice,
            self.model,
            self.SMOOTHING_RADIUS,
        )


if __name__ == "__main__":
    execution = pipelineExecutor()
    execution.main()
