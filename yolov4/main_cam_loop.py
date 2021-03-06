import cv2
from imutils.video import FPS
from yolov4.drawing import Drawing
from utils.init_cam import init_cam
from yolov4.lock import GestureLock


def main_cam(gesture_lock, phone_cam):
    cap, fps = init_cam(phone_cam)
    fps_count = 0.0
    W = cap.get(3)
    H = cap.get(4)
    # W = 1920
    # H = 1080
    drawing = Drawing(W, H)

    while True:
        frame = cap.read()
        frame = cv2.flip(frame, 1)
        gesture, action = gesture_lock.get_gesture()
        text = action + " (" + str(gesture) + ")"
        cv2.putText(frame, text=text, org=(30, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=3,
                    color=(0, 255, 20), thickness=5)
        frame = drawing.process_frame(frame, action)

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
