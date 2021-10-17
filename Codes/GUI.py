import json
import tkinter as tk
from Pipeline import callStabilize, callCompress, callFaceDetect, callLipExtraction, callTongueTrack, callConfigEditor, \
    callPerformAll


def a():
    callStabilize(MainFile, SMOOTHING_RADIUS)


def b():
    callCompress(MainFile)


def c():
    callFaceDetect(MainFile, correctionFactor_Face)


def d():
    callLipExtraction(MainFile, correctionFactor_Lip)


def e():
    callTongueTrack(MainFile, threshold,thresh_iterations, disp,visual_area, time_slice, model, save_in_excel)


def f():
    callConfigEditor()


def GUI(MainFile, SMOOTHING_RADIUS, threshold, thresh_iterations, visual_area, disp, correctionFactor_Face
        , correctionFactor_Lip, save_in_excel, time_slice, model):
    top = tk.Toplevel()
    top.title("Tongue Frequency Calculator")
    canvas_width = 500
    canvas_height = 10
    w = tk.Canvas(top,
                  width=canvas_width,
                  height=canvas_height)
    w.pack()
    background_image = tk.PhotoImage(
        file=r"C:/Users/budha/PycharmProjects/TongueFrequencyCalculator/Images/background.png")
    background_label = tk.Label(top, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    B1 = tk.Button(top, text="Stabilize Video", command=a, height=5, width=20)
    B2 = tk.Button(top, text="Compress Video", command=b, height=5, width=20)
    B3 = tk.Button(top, text="Perform Face Extraction", command=c, height=5, width=20)
    B4 = tk.Button(top, text="Perform Lip Extraction", command=d, height=5, width=20)
    B5 = tk.Button(top, text="Perform Tongue Movement Analysis", command=e,
                   height=5, width=20,
                   wraplength=120)

    B1.pack(side=tk.LEFT, padx=10)
    B2.pack(side=tk.RIGHT, padx=10)
    B3.pack(side=tk.TOP, pady=10)
    B4.pack(side=tk.TOP)
    B5.pack(side=tk.BOTTOM, pady=10)

    top.mainloop()


model = ""  # load_model("../../final_model.h5", compile=False)
# Global Variable Declaration
with open('temp.json', 'r') as openfile:
    json_object = json.load(openfile)

print(json_object)

values = json_object
SMOOTHING_RADIUS = values['0']
visual_area = values['1']
Height_Vid = values['2']
Width_Vid = values['3']
correctionFactor_Lip = values['4']
correctionFactor_Face = values['5']
threshold = values['6']
time_slice = values['7']
save_in_excel = values['8']
MainFile = values['9']
thresh_iterations = 2
disp = False
GUI(MainFile, SMOOTHING_RADIUS, threshold, thresh_iterations, visual_area, disp, correctionFactor_Face,
    correctionFactor_Lip, save_in_excel, time_slice, model)
