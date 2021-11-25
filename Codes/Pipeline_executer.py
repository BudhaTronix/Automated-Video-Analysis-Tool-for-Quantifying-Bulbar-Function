import glob
from Pipeline import pipeline
from keras.models import load_model


class pipelineExecutor:
    def __init__(self):
        self.model = load_model('final_model.h5', compile=False)
        # Global Variable Declaration
        self.use_GUI = True
        self.SMOOTHING_RADIUS = 50
        self.visual_area = 0  #
        self.correctionFactor_Face = 30
        self.correctionFactor_Lip = 30
        self.threshold = 40
        self.thresh_iterations = 2
        self.disp = False
        self.save_in_excel = True
        self.time_slice = 5
        # Change Base File Name
        self.MainFile = "C:\\Users\\budha\\PycharmProjects\\TongueFrequencyCalculator\\VideoFies\\37a.mov"
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
        # Change it to True if you want Stabilization
        if self.use_GUI:
            from GUI import GUI
            obj = GUI(self.model)
            obj.loaderFunc()

        else:
            obj = pipeline()
            if self.Multi_mode:
                for file_name in sorted(glob.iglob('*.mov')):
                    print("\n ################################################################# \n")
                    print("Working on File Name : ", file_name)
                    print("Processing Starts")
                    obj.CUI(file_name, self.Stabilize, self.Video_Compression, self.Face_Extract, self.Lip_Extraction,
                            self.Frquency_Calculation, self.threshold, self.thresh_iterations, self.visual_area,
                            self.disp,
                            self.correctionFactor_Face, self.correctionFactor_Lip,
                            self.save_in_excel, self.time_slice, self.model, self.SMOOTHING_RADIUS)
                    print("Processing Ends")
                    print("\n ################################################################# \n")
            else:
                obj.CUI(self.MainFile, self.Stabilize, self.Video_Compression, self.Face_Extract, self.Lip_Extraction,
                        self.Frquency_Calculation, self.threshold, self.thresh_iterations, self.visual_area, self.disp,
                        self.correctionFactor_Face, self.correctionFactor_Lip,
                        self.save_in_excel, self.time_slice, self.model, self.SMOOTHING_RADIUS)


execution = pipelineExecutor()
execution.main()

