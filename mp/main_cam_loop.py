import math

import cv2
from imutils.video import FPS
from mediapipe.python.solutions.hands import HAND_CONNECTIONS

from mp.drawing import Drawing
import mediapipe as mp

from utils.init_cam import init_cam
from utils.motion_analyser import MotionAnalyser


def _count_fingers(frame, detector, mp_drawing):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = detector.process(frame)
    frame.flags.writeable = True
    n_fingers_l, center_l, pointy_r, thickness = None, None, None, None

    if results.multi_hand_landmarks:
        for mh, lm in zip(results.multi_handedness, results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, lm, HAND_CONNECTIONS)
            label = mh.classification[0].label
            lm = lm.landmark
            if label == "Left":
                n_fingers_l = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (
                        lm[16].y < lm[15].y) + (lm[20].y < lm[19].y)
                center_l = (lm[9].x, lm[9].y)
            elif label == "Right":
                dist = math.sqrt(abs((lm[8].x - lm[0].x) + (lm[8].y - lm[0].y)))
                thickness = int(dist ** 4 * 150)
                if thickness < 1:
                    pointy_r = None
                else:
                    sh = frame.shape
                    pointy_r = (int(lm[8].x * sh[1]), int(lm[8].y * sh[0]))
    return n_fingers_l, center_l, pointy_r, thickness


def main_cam(phone_cam):
    cap, fps = init_cam(phone_cam)
    fps_count = 0.0
    W = cap.get(3)
    H = cap.get(4)
    # W = 1920
    # H = 1080
    drawing = Drawing(W, H)
    ma = MotionAnalyser(W, H)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    detector = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    pairs = {3: "Yellow", 5: "Erasing", 0: "Green", 2: "Brown", 1: "Blue", 4: "Black"}

    while True:
        frame = cap.read()
        frame = cv2.flip(frame, 1)
        n_fingers_l, center_l, pointy_r, thickness = _count_fingers(frame, detector, mp_drawing)
        if n_fingers_l is not None:
            action = pairs[n_fingers_l]
            text = action + " (" + str(n_fingers_l) + ") " + str(pointy_r)
        else:
            action = None
            text = "None"


        dx, dy, total_dx, total_dy = ma.analyse(center_l, n_fingers_l)

        frame = drawing.process_frame(frame, action, pointy_r, thickness)

        cv2.putText(frame, text=text, org=(30, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=3,
                    color=(0, 255, 20), thickness=5)
        fps.update()
        if fps._numFrames == 25:
            fps.stop()
            fps_count = fps.fps()
            fps = FPS().start()
        cv2.putText(frame, text=str(round(fps_count, 1)), org=(1350, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2, color=(0, 255, 20), thickness=3)

        cv2.imshow('Cam', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_cam(phone_cam=True)
