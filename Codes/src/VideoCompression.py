import moviepy.editor as mp
import cv2


def VideoCompression(Filename, New_Filename, Height_Vid=1200, Width_Vid=800):
    compression_possible = True
    print("Input File name  : ", Filename)
    print("Output File name : ", New_Filename)
    try:
        h = Height_Vid
        w = Width_Vid
        filename = Filename
        clip = mp.VideoFileClip(filename)
        clip_resized = clip.resize((h, w))
        clip_resized.write_videofile(New_Filename)
    except:
        # TRY USING OPENCV
        try:
            def resizer(pic, newsize):
                lx, ly = int(newsize[0]), int(newsize[1])
                if lx > pic.shape[1] or ly > pic.shape[0]:
                    # For upsizing use linear for good quality & decent speed
                    interpolation = cv2.INTER_LINEAR
                else:
                    # For dowsizing use area to prevent aliasing
                    interpolation = cv2.INTER_AREA
                return cv2.resize(+pic.astype('uint8'), (lx, ly),
                                  interpolation=interpolation)

            cap = cv2.VideoCapture(Filename)
            w = Width_Vid
            h = Height_Vid
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Define the codec for output video
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')

            # Set up output video
            out = cv2.VideoWriter(New_Filename, fourcc, fps, (h, w))

            n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            for i in range(n_frames - 2):
                success, frame = cap.read()
                if not success:
                    break

                out.write(resizer(frame, (h, w)))
            cap.release()
            out.release()
            # Close windows
            cv2.destroyAllWindows()
        except:
            compression_possible = False
            print("Please install either OpenCV or moviepy Editor")
            return compression_possible

    return compression_possible
