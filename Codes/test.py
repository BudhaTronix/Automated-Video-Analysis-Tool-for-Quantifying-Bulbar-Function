import StartUI
import GUI
import json

A = StartUI
A.loaderFunc()
exit(A)
B = GUI
with open('temp.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

print(json_object)
print(type(json_object))
print("test")
values = json_object
model = ""#load_model("../../final_model.h5", compile=False)
#Global Variable Declaration
SMOOTHING_RADIUS=values['0']
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
B.GUI(MainFile,SMOOTHING_RADIUS,threshold,thresh_iterations,visual_area,disp,correctionFactor_Face,correctionFactor_Lip,save_in_excel,time_slice,model)
