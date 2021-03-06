import math
import numpy as np
import cv2


class Drawing:
    def __init__(self, W, H):
        # self.purple_range = np.array([[120, 32, 182], [154, 255, 255]])  # purple boundaries in hsv
        self.purple_range = np.array([[31, 255, 139], [47, 255, 255]])  # purple boundaries in hsv
        # self.purple_range = np.array([[0, 0, 250], [255, int(0.05 * 255), 255]])  # white boundaries in hsv
        self.noiseth = 1  # threshold
        self.x1, self.y1 = 0, 0
        self.canvas = np.zeros((int(H), int(W), 3), dtype=np.uint8)
        self.previous_action = ""

    def process_frame(self, frame, action):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.purple_range[0], self.purple_range[1])
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            max_area = cv2.contourArea(max(contours, key=cv2.contourArea))
            if max_area > self.noiseth:
                contour = max(contours, key=cv2.contourArea)
                x2, y2, w, h = cv2.boundingRect(contour)
                x2 = int(x2 + w / 2)  # center of box
                y2 = int(y2 + h / 2)

                # # debug
                # self.canvas = cv2.circle(self.canvas, (x2, y2), color=[0, 0, 255], radius=25, thickness=-10)
                # return cv2.add(frame, self.canvas)

                # if we have same action, and coordinates of a pen from previous frame
                if action == self.ex_action and self.x1 != 0 and self.y1 != 0:
                    color = []
                    if action == "Erasing":
                        color = [0, 0, 0]
                    elif action == "Yellow":
                        color = [0, 255, 255]  # in BGR
                    elif action == "Brown":
                        color = [30, 40, 100]
                    elif action == "Green":
                        color = [0, 255, 0]
                    elif action == "Blue":
                        color = [255, 0, 0]
                    thickness = int(math.sqrt(max_area) / 1.5)
                    self.canvas = cv2.line(self.canvas, (self.x1, self.y1), (x2, y2), color, thickness=thickness)
                self.x1, self.y1 = x2, y2
            else:
                self.x1, self.y1 = 0, 0
        self.previous_action = action

        return cv2.add(frame, self.canvas)
