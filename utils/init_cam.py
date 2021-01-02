import cv2
from imutils.video import FPS


def init_cam(phone_cam):
    cap = cv2.VideoCapture(0)
    if phone_cam:
        # address = "http://192.168.1.193:8080/video"
        address = "http://192.168.137.203:8080/video"
        cap.open(address)
    fps = FPS().start()
    return cap, fps
