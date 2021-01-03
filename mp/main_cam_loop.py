import cv2
from imutils.video import FPS

from mp.drawing import Drawing
import mediapipe as mp

from mp.lock import GestureLock
from utils.init_cam import init_cam
from utils.motion_analyser import MotionAnalyser


def main_cam(gesture_lock, phone_cam):
    cap, fps = init_cam(phone_cam)
    fps_count = 0.0
    W = cap.get(3)
    H = cap.get(4)
    # W = 1920
    # H = 1080
    drawing = Drawing(W, H)
    pairs = {3: "Yellow", 5: "Erasing", 0: "Green", 2: "Brown", 1: "Blue", 4: "Black"}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('Video file finished.')
            break
        frame = cv2.resize(cv2.flip(frame, 1), dsize=(1920, 1080))
        n_fingers_l, pointy_r, thickness = gesture_lock.get_gesture()
        if n_fingers_l is not None:
            action = pairs[n_fingers_l]
        else:
            action = None
        text = str(action) + " (" + str(n_fingers_l) + ") " + str(pointy_r)

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

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_cam(gesture_lock=GestureLock(), phone_cam=True)
