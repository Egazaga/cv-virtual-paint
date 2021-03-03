import queue
import threading

import cv2
from imutils.video import FPS


# bufferless VideoCapture
class VideoCapture:
    def __init__(self, name, phone_cam):
        self.cap = cv2.VideoCapture(name)
        if phone_cam:
            address = "http://192.168.1.193:8080/video"
            self.cap.open(address)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def get(self, n):
        return self.cap.get(n)


def init_cam(phone_cam):
    cap = VideoCapture(0, phone_cam)
    fps = FPS().start()
    return cap, fps
