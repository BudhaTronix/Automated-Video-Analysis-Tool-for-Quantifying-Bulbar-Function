import json
import PySimpleGUI as sg
# from StartUI import loaderFunc
from Pipeline import callStabilize, callFaceDetect, callLipExtraction, callTongueTrack


def readJSON():
    with open('temp.json', 'r') as openfile:
        json_object = json.load(openfile)
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

    return SMOOTHING_RADIUS, visual_area, Height_Vid, Width_Vid, correctionFactor_Lip, correctionFactor_Face, threshold, time_slice, save_in_excel, MainFile


def loaderFunc_orig():
    t_len = 22

    preProc = [[sg.Button(size=(t_len, 4), button_text="Stabilize Video", ),
                sg.Button(size=(t_len, 4), button_text="Compress Video", )], ]
    FeatureExtrac = [[sg.Button(size=(t_len, 4), button_text="Perform Face Extraction", ),
                      sg.Button(size=(t_len, 4), button_text="Perform Lip Extraction", )], ]
    Analysis = [[sg.Button(size=(t_len, 4), button_text="Perform Tongue Movement Analysis", ),
                 sg.Button(size=(t_len, 1), button_text="Edit Configuration", )], ]

    layout = [[sg.Frame('Pre-Processing', preProc, title_color='white', font='Any 12')],
              [sg.Frame('Feature Extraction', FeatureExtrac, title_color='white', font='Any 12')],
              [sg.Frame('Analysis', Analysis, title_color='white', font='Any 12')], ]

    window = sg.Window('Automated Tongue Tracking Tool', font=("Helvetica", 12), element_justification='center').Layout(
        layout)

    button, values = window.Read()
    # print(button, values)

    SMOOTHING_RADIUS, visual_area, Height_Vid, Width_Vid, \
    correctionFactor_Lip, correctionFactor_Face, threshold, time_slice, save_in_excel, MainFile = readJSON()

    thresh_iterations = 0
    disp = False
    model = ""

    if button == "Edit Configuration":
        loaderFunc()
    elif button == "Compress Video":
        loaderFunc()
    elif button == "Stabilize Video":
        callStabilize(MainFile, SMOOTHING_RADIUS)
    elif button == "Perform Face Extraction":
        callFaceDetect(MainFile, correctionFactor_Face)
    elif button == "Perform Lip Extraction":
        callLipExtraction(MainFile, correctionFactor_Lip)
    elif button == "Perform Tongue Movement Analysis":
        callTongueTrack(MainFile, threshold, thresh_iterations, disp, visual_area, time_slice, model, save_in_excel)
    window.close()
    if button is not None:
        loaderFunc_orig()


def loaderFunc():
    length = 6
    t_len = 20

    parms = [[sg.Text('Blur Smoothening Radius', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=50, size=(length, 1)),
              sg.Text('Visual Area Correction', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=0, size=(length, 1))],

             [sg.Text('Video Height', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 10000)], initial_value=1200, size=(length, 1)),
              sg.Text('Video Breadth', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 10000)], initial_value=800, size=(length, 1))],

             [sg.Text('Lip Correction Factor', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=30, size=(length, 1)),
              sg.Text('Tongue Correction Factor', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=30, size=(length, 1))],

             [sg.Text('Threshold', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=40, size=(length, 1)),
              sg.Text('Time Slice', size=(t_len, 1)),
              sg.Spin(values=[i for i in range(1, 100)], initial_value=5, size=(length, 1))],

             [sg.Text('Save in Excel', size=(t_len, 1)),
              sg.Drop(values=('true', 'false'), default_value="true", auto_size_text=True),
              sg.Text('Start Filename', size=(t_len, 1)), sg.In(default_text="37a.mov", size=(8, 1)), ],]

    layout = [[sg.Frame('Parameteres', parms, title_color='black', font='Any 12')],
              [sg.Submit(size=(20, 1), button_text="Save Configuration", ), sg.Cancel(size=(15, 1))]]
    window = sg.Window('Automated Tongue Tracking Tool - Configuration', font=("Helvetica", 12),
                       element_justification='center').Layout(layout)

    button, values = window.Read()

    window.close()
    with open("temp.json", "w") as outfile:
        json.dump(values, outfile)


loaderFunc_orig()
