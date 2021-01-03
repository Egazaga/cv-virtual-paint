import math

import cv2
import keyboard
import mediapipe as mp
from mediapipe.python.solutions.hands import HAND_CONNECTIONS

from utils.init_cam import init_cam
from mp.lock import GestureLock
from utils.motion_analyser import MotionAnalyser


def _count_fingers(frame, detector):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = detector.process(frame)
    frame.flags.writeable = True
    n_fingers_l, pointy_r, thickness = None, None, None

    if results.multi_hand_landmarks:
        for mh, lm in zip(results.multi_handedness, results.multi_hand_landmarks):
            # mp_drawing.draw_landmarks(frame, lm, HAND_CONNECTIONS)
            label = mh.classification[0].label
            lm = lm.landmark
            if label == "Left":
                n_fingers_l = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (
                            lm[16].y < lm[15].y) + (lm[20].y < lm[19].y)
            elif label == "Right":
                dist = math.sqrt(abs((lm[8].x - lm[0].x) + (lm[8].y - lm[0].y)))
                thickness = int(dist ** 4 * 150)
                if thickness < 1:
                    pointy_r = None
                else:
                    sh = frame.shape
                    pointy_r = (int(lm[8].x * sh[1]), int(lm[8].y * sh[0]))
    return n_fingers_l, pointy_r, thickness


def mediapipe_detection(gesture_lock, phone_cam):
    mp_hands = mp.solutions.hands
    detector = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

    cap, fps = init_cam(phone_cam)
    W = cap.get(3)
    H = cap.get(4)
    ma = MotionAnalyser(W, H)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('Video file finished.')
            break
        frame = cv2.flip(frame, 1)
        n_fingers_l, pointy_r, thickness = _count_fingers(frame, detector)
        gesture_lock.set_gesture(n_fingers_l, pointy_r, thickness)

        fps.update()
        if keyboard.is_pressed('esc'):  # can't use cv's waitKey, cuz no window
            break

    fps.stop()
    print("Mean fps for detection:", round(fps.fps(), 2))
    cap.release()


if __name__ == '__main__':
    mediapipe_detection(gesture_lock=GestureLock(), phone_cam=True)
