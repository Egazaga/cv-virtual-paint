import math
from operator import add

import numpy as np
import cv2

hsv = (155, 117, 139)
hsv = np.uint8([[[hsv[2], hsv[1], hsv[0]]]])
hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)[0][0]
hsv = np.array([int(hsv[0] / 2), int(hsv[1] / 100 * 255), int(hsv[2] / 100 * 255)])
dc = 20


class Drawing:
    def __init__(self, W, H):
        self.purple_range = np.array([[0, 0, 250], [255, int(0.05 * 255), 255]])  # purple boundaries in hsv
        self.purple_range = np.array([hsv - dc, hsv + dc])  # purple boundaries in hsv
        self.noiseth = 100  # threshold
        self.ex_pen_pos = 0, 0
        self.ex_action = None
        self.canvas = np.zeros((int(H * 3), int(W * 3), 3), dtype=np.uint8)
        self.view_center = int(W * 1.5), int(H * 1.5)
        cv2.circle(self.canvas, self.view_center, color=[0, 0, 255], radius=25, thickness=-10)  # debug
        for x in range(3):
            for y in range(3):
                cv2.circle(self.canvas, (int(W * x), int(H * y)), color=[0, 0, 255], radius=25, thickness=-10)  # debug
        # for i in range(100):
        #     cv2.circle(self.canvas, (100 * i, 1200), color=[0, 0, 255], radius=25, thickness=-10)  # debug
        self.view_corner = int(W), int(H)
        self.scale_factor = 1
        self.W, self.H = int(W), int(H)

    def find_pen(self, frame):
        x, y, w, h, area = None, None, None, None, None
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.purple_range[0], self.purple_range[1])
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            area = cv2.contourArea(max(contours, key=cv2.contourArea))
            if area > self.noiseth:
                contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(contour)
                x = int(x + w / 2)  # center of box
                y = int(y + h / 2)
        return x, y, area

    def process_frame(self, frame, x, y, area, action):
        if x is None:
            self.ex_action = None
            self.ex_pen_pos = 0, 0
        elif action != self.ex_action:
            self.ex_action = action
            self.ex_pen_pos = 0, 0
        elif self.ex_pen_pos == (0, 0):
            self.ex_pen_pos = (x + self.view_corner[0], y + self.view_corner[1])
        else:  # if we have same action, and coordinates of a pen from previous frame
            color = []
            thickness = int(math.sqrt(area) / 1.5)
            if action == "Erasing":
                color = [0, 0, 0]
                thickness = 90
            elif action == "Yellow":
                color = [0, 255, 255]  # in BGR
            elif action == "Brown":
                color = [30, 40, 100]
            elif action == "Green":
                color = [0, 255, 0]
            elif action == "Blue":
                color = [255, 0, 0]
            elif action == "Black":
                color = [255, 255, 255]
            pt1 = (self.ex_pen_pos[0] + self.view_corner[0], self.ex_pen_pos[1] + self.view_corner[1])
            pt2 = (x + self.view_corner[0], y + self.view_corner[1])
            self.canvas = cv2.line(self.canvas, pt1, pt2, color, thickness=thickness)
            self.ex_pen_pos = (x + self.view_corner[0], y + self.view_corner[1])

        view = self.canvas[self.view_corner[1]:self.view_corner[1] + int(self.H / self.scale_factor),
               self.view_corner[0]:self.view_corner[0] + int(self.W / self.scale_factor)]
        if self.scale_factor != 1:
            view = cv2.resize(view, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        return cv2.addWeighted(frame, 1, view, 0.7, 0)

    def move(self, dx, dy):
        move_x, move_y = 0, 0
        if self.view_corner[0] != 0 and self.view_corner[0] != self.W * 3 - self.W / self.scale_factor:
            move_x = int(-dx / self.scale_factor)
        if self.view_corner[1] != 0 and self.view_corner[1] != self.H * 3 - self.H / self.scale_factor:
            move_y = int(-dy / self.scale_factor)
        self.view_corner = tuple(map(add, self.view_corner, (move_x, move_y)))

    def scale(self, dy):
        if (self.scale_factor > 2.9 and dy < 0) or (self.scale_factor < 0.1 and dy > 0):
            return
        else:
            self.scale_factor -= dy / 700
