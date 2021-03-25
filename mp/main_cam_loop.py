import cv2
import mediapipe as mp
from imutils.video import FPS

from mp.drawing import Drawing
from utils.init_cam import init_cam
from utils.motion_analyser import MotionAnalyser


def _count_fingers(frame, detector, hand="Left"):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = detector.process(frame)
    frame.flags.writeable = True
    n_fingers_l, center_l = None, None

    if results.multi_hand_landmarks:
        for mh, lm in zip(results.multi_handedness, results.multi_hand_landmarks):
            # mp_drawing.draw_landmarks(frame, lm, HAND_CONNECTIONS)
            label = mh.classification[0].label
            lm = lm.landmark
            if label == hand:
                n_fingers_l = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (
                        lm[16].y < lm[15].y) + (lm[20].y < lm[19].y)
                sh = frame.shape
                center_l = (lm[9].x * sh[1], lm[9].y * sh[0])
    return n_fingers_l, center_l


def callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = param[0]
        drawing.set_pen_color(param[1][y, x])


def main_cam(phone_cam, video_path=None, imgs_paths=None):
    cap, fps = init_cam(phone_cam, video_path, imgs_paths)
    fps_count = 0.0
    W = cap.get(3)
    H = cap.get(4)
    drawing = Drawing(W, H)
    ma = MotionAnalyser(W, H, drawing)
    mp_hands = mp.solutions.hands
    detector = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    pairs = {3: "Yellow", 5: "Erasing", 0: "Green", 2: "Brown", 1: "Blue", 4: "Black"}
    cv2.namedWindow("Cam", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Cam", cv2.WND_PROP_FULLSCREEN, 1)

    while True:
        frame = cap.read()
        if frame is None:
            print("End of sequence")
            break
        frame = cv2.flip(frame, 1)
        cv2.setMouseCallback('Cam', callback, (drawing, frame))
        n_fingers_l, center_l = _count_fingers(frame, detector)
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
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    return drawing, ma  # for testing


if __name__ == '__main__':
    main_cam(phone_cam=True)
