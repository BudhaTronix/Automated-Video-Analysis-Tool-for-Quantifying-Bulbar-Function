import moviepy.editor
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import statistics


def plot(arr):
    x = np.arange(1, len(arr) + 1, 1)
    y = arr
    plt.scatter(x, y, label="Sweep duration", color="green",
                marker="*", s=20)
    # x-axis label
    plt.xlabel('Sweep Number')
    # frequency label
    plt.ylabel('Number of Frames')
    # plot title
    plt.title('Sweep Durations')
    # showing legend
    plt.legend()

    # function to show the plot
    plt.show()


def make_square(img):
    IMAGE_SIZE = 256
    im = Image.fromarray(img)
    fill_color = (0, 0, 0, 0)
    min_size = IMAGE_SIZE
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    open_cv_image = np.array(new_im)
    i = cv2.resize(open_cv_image, (256, 256), interpolation=cv2.INTER_CUBIC)
    return i


def mask_parse(mask):
    mask = np.squeeze(mask)
    mask = [mask, mask, mask]
    mask = np.transpose(mask, (1, 2, 0))
    return mask


def calFreq(arr):
    arr2 = np.array([['X'], [2]])
    start = 'R'
    count = 0
    for x in arr:
        if x == start:
            count = count + 1
        else:
            arr2 = np.append(arr2, (start, count))
            count = 1
            if start == "L":
                start = "R"
            else:
                start = "L"
    arr2 = np.append(arr2, (start, count))
    arr2 = arr2.reshape(int(len(arr2) / 2), 2)
    arr2 = np.delete(arr2, 0, 0)
    l = len(arr2)
    sweeps = []
    for index, obj in enumerate(arr2):
        if index < (l - 1):
            next = arr2[index + 1]
            total_frames = int(obj[1]) / 2 + int(next[1]) / 2
            sweeps.append(total_frames)

    return sweeps


def outlier_detector(data_1):
    dataset = data_1
    dataset = sorted(dataset)
    q1, q3 = np.percentile(dataset, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    print("Lower Bound: ", lower_bound)
    print("Upper Bound: ", upper_bound)
    outliers = []
    index = []
    array = []
    for i, y in enumerate(data_1):
        if y > upper_bound:
            outliers.append(y)
            index.append(i)
        elif y < lower_bound:
            outliers.append(y)
            index.append(i)
        else:
            array.append(y)
    return outliers, index, array


def FrequencyCalculation(Filename, threshold, thresh_iterations, visual_area, disp, time_slice, model):
    print("Using Lip Segmentation Model")
    # Video Slicing
    print("Input File used : ", Filename)
    New_Filename = "../../tmp/tmp.mp4"

    video = moviepy.editor.VideoFileClip(Filename)
    video_duration = int(video.duration)
    time_slice = time_slice
    if video_duration > time_slice:
        start_time = (video_duration - time_slice) / 2
        end_time = ((video_duration + time_slice) / 2)
    else:
        print("Video File smaller than time slice")
        start_time = 0
        end_time = video_duration
        time_slice = video_duration
    print("Video Duration: ", video_duration)
    print("Start time:     ", start_time)
    print("End time:       ", end_time)
    ffmpeg_extract_subclip(Filename, start_time, end_time, targetname=New_Filename)
    time.sleep(5)
    # Reading the clipped file
    cap = cv2.VideoCapture(New_Filename)
    fps = cap.get(cv2.CAP_PROP_FPS)

    columns = 256
    arr = np.array(['R'])
    while True:
        success, frame = cap.read()
        if success:
            x = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            x = make_square(x)
            x = x / 255.0
            y_pred_orig = model.predict(np.expand_dims(x, axis=0))[0] > 0.5
            y_pred = y_pred_orig * 1
            h, w, _ = x.shape
            white_line = np.ones((h, 10, 3))
            all_images = [
                x, white_line,
                mask_parse(y_pred)
            ]

            image = np.concatenate(all_images, axis=1)
            thresh = y_pred
            left = thresh[:, :int(columns / 2) - visual_area]
            right = thresh[:, int(columns / 2) + visual_area:columns]
            l = left.flatten().sum(axis=0)
            r = right.flatten().sum(axis=0)
            activation = 1000
            if (r > l) and (r > activation):
                if disp: print("Right", "R:", r, "  L:", l, "   Difference:", abs(r - l),
                               "Previous direction:", arr[-1])
                arr = np.append(arr, "R ")
                if disp:
                    plt.imshow(image)
                    plt.show()
            elif (l > r) and (l > activation):
                if disp: print("Left", "R:", r, "  L:", l, "   Difference:", abs(r - l),
                               "Previous direction:", arr[-1])
                arr = np.append(arr, "L ")
                if disp:
                    plt.imshow(image)
                    plt.show()
            else:
                arr = np.append(arr, arr[-1])
                if disp:
                    print("Cannot see, Selected :", arr[-1], "  Detection: ", r, l)
                    plt.imshow(image)
                    plt.show()

        else:
            break
    # Close windows
    cap.release()
    cv2.destroyAllWindows()

    sweeps = calFreq(arr)
    plot(sweeps)

    print("\n#####################################")
    print("Total number of sweeps: ", len(sweeps))
    print("Detecting outliers.......")  # outliers,index,array
    outliers, index, array = outlier_detector(sweeps)
    print("Number of outliers: ", len(outliers))
    print("Accepted Sweeps:    ", len(array))
    if len(outliers) > 0:
        print("Outliers detected at:")
        for i in index:
            print("Sweep Location: ", i, "    Sweep Duration: ", sweeps[i])

    try:
        mode = statistics.mode(sweeps)
    except:
        mode = 1
        print("Error in Mode calculation")

    try:
        mean = np.average(sweeps)
    except:
        mean = 1
        print("Error in Mean calculation")

    try:
        stdev = statistics.stdev(sweeps)
    except:
        stdev = 1
        print("Error in StDev calculation")

    print("Mode: ", mode)
    print("Mean: ", mean)
    print("SD  : ", stdev)
    print("#########################################\n")
    return len(sweeps), len(outliers), mode, mean, stdev, fps, time_slice