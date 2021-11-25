import cv2
# import torch
from facenet_pytorch import MTCNN


def FaceExtraction(Filename, New_Filename, correctionFactor):
    print("Input File name  : ", Filename)
    print("Output File name : ", New_Filename)
    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device = "cpu"

    print('Running on device: {}'.format(device))
    mtcnn = MTCNN(margin=40, select_largest=False, post_process=False, device=device)

    cap = cv2.VideoCapture(Filename)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    Y1 = Y2 = X1 = X2 = 0

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    c = 0
    for i in range(n_frames):
        success, frame = cap.read()
        if not success:
            break
        # Add to batch
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print('\rTracking frame: {}'.format(i + 1), end='')

        # Detect faces
        boxes, prob, landmarks = mtcnn.detect(frame, landmarks=True)
        if boxes is None:
            True
        else:
            c = c + 1
            x1_f = int(boxes[0][0])
            y1_f = int(boxes[0][1])
            w = int(boxes[0][2])
            h = int(boxes[0][3])

            Y1 = Y1 + y1_f
            Y2 = Y2 + h
            X1 = X1 + x1_f
            X2 = X2 + w

    cf = correctionFactor
    if c == 0:
        Y1_avg = Y2_avg = X1_avg = X2_avg = 0
    else:
        Y1_avg = int(Y1 / c)
        Y2_avg = int(Y2 / c)
        X1_avg = int(X1 / c)
        X2_avg = int(X2 / c)

    if Y1_avg - cf < 1: Y1_avg = cf
    if Y2_avg < 1: Y2_avg = 0
    if X1_avg - cf < 1: X1_avg = cf
    if X2_avg < 1: X2_avg = 0

    print(Y1_avg, Y2_avg, X1_avg, X2_avg, c)
    cap2 = cv2.VideoCapture(Filename)

    w = int((cap2.get(cv2.CAP_PROP_FRAME_WIDTH)) * .5)
    h = int((cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)) * .75)
    fps = cap2.get(cv2.CAP_PROP_FPS)
    # Define the codec for output video
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # Set up output video
    out = cv2.VideoWriter(New_Filename, fourcc, fps, (w, h))
    shape = w, h
    while True:
        success, frame = cap2.read()
        if success:
            crop_img = frame[Y1_avg - cf:Y2_avg + cf, X1_avg - cf:X2_avg + cf]
            cv2.waitKey(10)
            out.write(cv2.resize(crop_img, shape))
        else:
            break
            # Close windows
    cap2.release()
    cap.release()
    out.release()
