import cv2
import keyboard
import mediapipe as mp

from utils.init_cam import init_cam
from mp.lock import GestureLock
from utils.motion_analyser import MotionAnalyser


def count_fingers(frame, detector):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = detector.process(frame)
    if results.multi_hand_landmarks:
        for mh in results.multi_handedness:
            label = mh.classification[0].label
            if label == "Left":
                lm = results.multi_hand_landmarks[0].landmark
                n = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (lm[16].y < lm[15].y) + (
                        lm[20].y < lm[19].y)
                return n


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
        n = count_fingers(frame, detector)
        print(n)
        if n is not None:
            gesture_lock.set_gesture(n)

        fps.update()
        if keyboard.is_pressed('esc'):  # can't use cv's waitKey, cuz no window
            break

    fps.stop()
    print("Mean fps for detection:", round(fps.fps(), 2))
    cap.release()


if __name__ == '__main__':
    mediapipe_detection(gesture_lock=GestureLock(True), phone_cam=False)
