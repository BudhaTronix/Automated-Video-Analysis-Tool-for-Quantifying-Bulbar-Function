import glob
from Pipeline import CUI
from keras.models import load_model


def main():
    model = load_model('final_model.h5', compile=False)
    # Global Variable Declaration
    use_GUI = True
    SMOOTHING_RADIUS = 50
    visual_area = 0  #
    correctionFactor_Face = 30
    correctionFactor_Lip = 30
    threshold = 40
    thresh_iterations = 2
    disp = False
    save_in_excel = True
    time_slice = 5
    MainFile = "C:\\Users\\budha\\PycharmProjects\\TongueFrequencyCalculator\\VideoFies\\37a.mov"  # Change When needed
    # Change it to True if you want Stabilization
    if use_GUI:
        from GUI import GUI
        obj = GUI(model)
        obj.loaderFunc()

    else:
        Stabilize = False

        # Change it to True if you want Video to be compressed
        Video_Compression = False

        # Change it to True if you want Face Extraction
        Face_Extract = True

        # Change it to True if you want Tongue Extraction
        Lip_Extraction = True

        # Change it to True if you want to calculate the frequency
        Frquency_Calculation = True

        # Change it to True if you want to run on All files
        Multi_mode = True

        if Multi_mode:
            for file_name in sorted(glob.iglob('*.mov')):
                print("\n ################################################################# \n")
                print("Working on File Name : ", file_name)
                print("Processing Starts")
                MainFile = file_name
                CUI(MainFile, Stabilize, Video_Compression, Face_Extract, Lip_Extraction, Frquency_Calculation,
                    threshold, thresh_iterations,
                    visual_area, disp,
                    correctionFactor_Face,
                    correctionFactor_Lip,
                    save_in_excel,
                    time_slice,
                    model)
                print("Processing Ends")
                print("\n ################################################################# \n")
        else:
            CUI(MainFile, Stabilize, Video_Compression, Face_Extract, Lip_Extraction, Frquency_Calculation,
                threshold, thresh_iterations,
                visual_area, disp,
                correctionFactor_Face,
                correctionFactor_Lip,
                save_in_excel,
                time_slice,
                model,SMOOTHING_RADIUS)


# if __name__ == "__main__":
main()
