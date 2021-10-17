import os
import os.path
from GUI import GUI
import glob
from keras.models import load_model
from Pipeline import CUI


def main():
    model = load_model("../model_weights/final_model.h5", compile=False)
    # Global Variable Declaration
    SMOOTHING_RADIUS = 50
    visual_area = 0  #
    correctionFactor_Face = 30
    correctionFactor_Lip = 30
    threshold = 40
    thresh_iterations = 2
    disp = False
    save_in_excel = True
    time_slice = 5
    MainFile = "37a.mov"  # Change When needed
    try:
        import google.colab
        IN_COLAB = True
    except:
        IN_COLAB = False
    if IN_COLAB == True:
        print('Running on CoLab')
        # drive.mount('/content/drive')
        os.chdir('/content/drive/My Drive/WORK/Work_OVGU_IKND/Codes/CurrentImplementation/Videos/Newset')

        # Change it to True if you want Stabilization
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
            for file_name in sorted(glob.iglob('*.mp4')):
                if ("_Stabilized" in file_name) or ("_Compressed" in file_name) or ("_FaceDetector" in file_name) or \
                        ("_LipDetector" in file_name):
                    print("")
                else:
                    print("\n ################################################################# \n")
                    print("Working on File Name : ", file_name)
                    print("Processing Starts")
                    MainFile = file_name
                    CUI(MainFile, Stabilize, Video_Compression, Face_Extract, Lip_Extraction, Frquency_Calculation,
                        SMOOTHING_RADIUS,
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
                SMOOTHING_RADIUS,
                threshold, thresh_iterations,
                visual_area, disp,
                correctionFactor_Face,
                correctionFactor_Lip,
                save_in_excel,
                time_slice,
                model)
    else:
        print('Running on Local System')
        GUI(MainFile, SMOOTHING_RADIUS, threshold, thresh_iterations, visual_area, disp, correctionFactor_Face,
            correctionFactor_Lip, save_in_excel, time_slice, model)


def callPerformAll():
    print("Starting....\n")
    CUI(MainFile, True, True, True, True, True, SMOOTHING_RADIUS, threshold, thresh_iterations, visual_area, disp
        , correctionFactor_Face, correctionFactor_Lip, model)
    # os.system('python Controller')
    print("Done!\n\n")


if __name__ == "__main__":
    main()
