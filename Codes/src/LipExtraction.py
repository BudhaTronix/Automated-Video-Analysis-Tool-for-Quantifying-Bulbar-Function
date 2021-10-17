import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from facenet_pytorch import MTCNN


def LipExtraction(Filename, New_Filename, correctionFactor):
    print("Input File name : ", Filename)
    print("Output File name : ", New_Filename)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    cf = correctionFactor
    print('Running on device: {}'.format(device))
    mtcnn = MTCNN(margin=40, select_largest=False, post_process=False, device=device)

    cap = cv2.VideoCapture(Filename)
    Y1 = Y2 = X1 = X2 = 0

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    arr_Y1 = arr_Y2 = arr_X1 = arr_X2 = [0]
    c = 0
    for i in range(n_frames):
        success, frame = cap.read()
        if not success:
            break

        # Add to batch
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, prob, landmarks = mtcnn.detect(frame, landmarks=True)
        if boxes is None:
            True
        else:
            c = c + 1
            x1 = int(landmarks[0][3][0])
            y1 = int(landmarks[0][3][1])
            x2 = int(landmarks[0][4][0])
            y2 = int(landmarks[0][4][1])

            if c == 1:
                crop_lip = frame[y1 - cf:y2 + cf, x1 - cf:x2 + cf]
                plt.imshow(crop_lip), plt.title('Original')
                plt.show()
                arr_Y1[0] = y1
                arr_Y2[0] = y2
                arr_X1[0] = x1
                arr_X2[0] = x2

            # Adding all the points
            Y1 = Y1 + y1
            Y2 = Y2 + y2
            X1 = X1 + x1
            X2 = X2 + x2

            # storing all the points
            arr_Y1 = np.append(arr_Y1, y1)
            arr_Y2 = np.append(arr_Y2, y2)
            arr_X1 = np.append(arr_X1, x1)
            arr_X2 = np.append(arr_X2, x2)

    counter = n_frames
    Y1_avg = int(Y1 / c)
    Y2_avg = int(Y2 / c)
    X1_avg = int(X1 / c)
    X2_avg = int(X2 / c)
    print(Y1_avg, Y2_avg, X1_avg, X2_avg, counter)
    print(np.amin(arr_Y1), np.amax(Y2_avg), np.amin(X1_avg), np.amax(X2_avg))
    cap2 = cv2.VideoCapture(Filename)

    w = int((cap2.get(cv2.CAP_PROP_FRAME_WIDTH)) * .75)
    h = int((cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)) * .5)
    fps = cap2.get(cv2.CAP_PROP_FPS)
    # Define the codec for output video
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # Set up output video
    out = cv2.VideoWriter(New_Filename, fourcc, fps, (w, h))
    shape = w, h
    while True:
        success, frame = cap2.read()
        if success:
            crop_img = frame[np.amin(arr_Y1) - cf:np.amax(Y2_avg) + cf, np.amin(X1_avg) - cf:np.amax(X2_avg) + cf]
            # cv2.waitKey(10)
            out.write(cv2.resize(crop_img, shape))
        else:
            break
            # Close windows
    cap2.release()
    cap.release()
    out.release()
