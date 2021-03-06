import cv2
import mediapipe as mp
from imutils.video import FPS

from mp.count_fingers import count_fingers
from mp.drawing import Drawing
from utils.init_cam import init_cam
from utils.motion_analyser import MotionAnalyser
from mp.logger import Logger


def callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = param[0]
        drawing.set_pen_color(param[1][y, x])


def main_cam(phone_cam, video_path=None, imgs_paths=None, default_pen_color=None):
    cap, fps = init_cam(phone_cam, video_path, imgs_paths)
    fps_count = 0.0
    W = cap.get(3)
    H = cap.get(4)
    drawing = Drawing(W, H, default_pen_color)
    ma = MotionAnalyser(W, H, drawing)
    logger = Logger(drawing, ma)
    mp_hands = mp.solutions.hands
    detector = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    pairs = {3: "Yellow", 5: "Erasing", 0: "Green", 2: "Brown", 1: "Blue", 4: "Black"}
    cv2.namedWindow("Cam", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Cam", cv2.WND_PROP_FULLSCREEN, 1)

    n_skipped_frames = 0

    while True:
        frame = cap.read()
        if isinstance(frame, tuple):
            frame = frame[1]
        if frame is None or frame.size == 0:
            n_skipped_frames += 1
            print("Skipped", n_skipped_frames)
            if n_skipped_frames == 90:
                print("End of sequence")
                break
            continue
        frame = cv2.flip(frame, 1)
        cv2.setMouseCallback('Cam', callback, (drawing, frame))
        n_fingers_l, center_l = count_fingers(frame, detector)
        x, y, area = drawing.find_pen(frame)
        if x is None:  # no pen in frame
            ma.analyse(center_l, n_fingers_l)

        if n_fingers_l is not None:
            action = pairs[n_fingers_l]
            text = action + " (" + str(n_fingers_l) + ") "
        else:
            action = None
            text = "None "

        frame = drawing.process_frame(frame, x, y, area, action)
        cv2.putText(frame, text=text + str(x), org=(30, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                    color=(0, 255, 20), thickness=3)
        fps.update()
        if fps._numFrames == 25:
            fps.stop()
            fps_count = fps.fps()
            fps = FPS().start()
        cv2.putText(frame, text=str(round(fps_count, 1)), org=(1750, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2, color=(0, 255, 20), thickness=3)
        cv2.putText(frame, text=str(round(drawing.scale_factor, 2)), org=(1750, 1000),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2, color=(0, 255, 20), thickness=3)

        cv2.imshow('Cam', frame)
        logger.log(n_fingers_l, center_l, (x, y), area)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    return logger


if __name__ == '__main__':
    main_cam(phone_cam=True)
