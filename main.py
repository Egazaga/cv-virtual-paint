from concurrent.futures.thread import ThreadPoolExecutor

from main_cam_loop import main_cam
from yolo_detection_loop import yolo_detection
from utils.gesture_lock import GestureLock


if __name__ == '__main__':
    lock = GestureLock()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(main_cam, lock)
        executor.submit(yolo_detection, lock)
