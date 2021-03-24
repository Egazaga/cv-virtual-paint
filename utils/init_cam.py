import glob
import queue
import threading

import cv2
from imutils.video import FPS


# bufferless VideoCapture
class MyVideoCapture:
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


class ImgSequenceCapture:
    def __init__(self, imgs_paths):
        self.imgs_paths = imgs_paths
        self.current_frame = 0

    def read(self):
        if self.current_frame == len(self.imgs_paths):
            return None
        img = cv2.imread(self.imgs_paths[self.current_frame], cv2.IMREAD_COLOR)
        self.current_frame += 1
        return img

    def get(self, n):
        print(self.imgs_paths[0])
        if n == 3:
            return cv2.imread(self.imgs_paths[0], cv2.IMREAD_COLOR).shape[1]
        if n == 4:
            return cv2.imread(self.imgs_paths[0], cv2.IMREAD_COLOR).shape[0]


def init_cam(phone_cam, video_path=None, imgs_paths=None):
    if video_path is not None:
        cap = cv2.VideoCapture(video_path)
    elif imgs_paths is not None:
        cap = ImgSequenceCapture(imgs_paths)
    else:
        cap = MyVideoCapture(0, phone_cam)
    fps = FPS().start()
    return cap, fps
