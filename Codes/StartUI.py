import json
import PySimpleGUI as sg
from time import sleep


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
              sg.Text('Start Filename', size=(t_len, 1)), sg.In(default_text="37a.mov", size=(8, 1)), ],

             ]

    layout = [[sg.Frame('Parameteres', parms, title_color='black', font='Any 12')],
              [sg.Submit(size=(20, 1), button_text="Save Configuration", ), sg.Cancel(size=(15, 1))]]
    window = sg.Window('Automated Tongue Tracking Tool - Configuration', font=("Helvetica", 12),
                       element_justification='center').Layout(layout)

    button, values = window.Read()

    window.close()
    with open("temp.json", "w") as outfile:
        json.dump(values, outfile)

loaderFunc()