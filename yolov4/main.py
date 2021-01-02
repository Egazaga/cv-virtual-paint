from concurrent.futures.thread import ThreadPoolExecutor

from yolov4.main_cam_loop import main_cam
from mp.mediapipe_detection_loop import mediapipe_detection
from yolov4.yolo_detection_loop import yolo_detection
from yolov4.lock import GestureLock


if __name__ == '__main__':
    phone_cam = True
    mediapipe_backend = True
    lock = GestureLock(mediapipe_backend)
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(main_cam, lock, phone_cam)
        if mediapipe_backend:
            executor.submit(mediapipe_detection, lock, phone_cam)
        else:
            executor.submit(yolo_detection, lock, phone_cam)
