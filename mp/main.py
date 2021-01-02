from concurrent.futures.thread import ThreadPoolExecutor

from mp.main_cam_loop import main_cam
from mp.mediapipe_detection_loop import mediapipe_detection
from mp.lock import GestureLock


if __name__ == '__main__':
    phone_cam = True
    lock = GestureLock()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(main_cam, lock, phone_cam)
        executor.submit(mediapipe_detection, lock, phone_cam)
