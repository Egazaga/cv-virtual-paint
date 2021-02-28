import math
from operator import add

import cv2
import numpy as np


class Drawing:
    def __init__(self, W, H):
        self.d_color_range = np.array([20, 50, 50])
        init_pen_color = np.array([174, 166, 223])
        self.pen_color_range = np.array([init_pen_color - self.d_color_range, init_pen_color + self.d_color_range])
        self.noise_threshold = 200
        self.ex_pen_pos = 0, 0
        self.ex_action = None
        self.canvas = np.zeros((int(H * 3), int(W * 3), 3), dtype=np.uint8)
        self.view_center = int(W * 1.5), int(H * 1.5)
        cv2.circle(self.canvas, self.view_center, color=[0, 0, 255], radius=25, thickness=-10)  # debug
        for x in range(4):
            for y in range(4):
                cv2.circle(self.canvas, (int(W * x), int(H * y)), color=[0, 0, 255], radius=25, thickness=-10)  # debug
        self.view_corner = int(W), int(H)
        self.scale_factor = 1
        self.W, self.H = int(W), int(H)
        self.thickness_scale = 2

    def set_pen_color(self, color):
        color = cv2.cvtColor(np.array([[color]], dtype="uint8"), cv2.COLOR_BGR2HSV)[0, 0]  # brg to hsv
        print("Set", color)
        self.pen_color_range = np.array([color - self.d_color_range, color + self.d_color_range])
        self.pen_color_range = np.where(self.pen_color_range < 0, 0, self.pen_color_range)

    def find_pen(self, frame):
        x, y, w, h, area = None, None, None, None, None
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.pen_color_range[0], self.pen_color_range[1])
        # self.canvas[1080:2160, 1920:3840] = np.stack((mask, mask, mask), axis=2)  # debug
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            area = cv2.contourArea(max(contours, key=cv2.contourArea))
            if area > self.noise_threshold:
                contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(contour)
                x = int(x + w / 2)  # center of box
                y = int(y + h / 2)
        return x, y, area

    def process_frame(self, frame, x, y, area, action):
        print(x, y)
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
            thickness = int(math.sqrt(area) * self.thickness_scale)
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

            pt2 = (x + self.view_corner[0], y + self.view_corner[1])
            self.canvas = cv2.line(self.canvas, self.ex_pen_pos, pt2, color, thickness=thickness)
            self.ex_pen_pos = pt2

        view = self.canvas[self.view_corner[1]:self.view_corner[1] + int(self.H * self.scale_factor),
               self.view_corner[0]:self.view_corner[0] + int(self.W * self.scale_factor)]
        if self.scale_factor != 1:
            view = cv2.resize(view, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        return cv2.addWeighted(frame, 0.5, view, 0.68, 0)

    def move(self, dx, dy, speed=2.5):
        move_x = int(-dx * self.scale_factor * speed)
        move_y = int(-dy * self.scale_factor * speed)

        if (self.view_corner[0] + move_x < 0) or \
                (self.view_corner[0] + move_x + self.W * self.scale_factor > 3 * self.W):
            move_x = 0

        if (self.view_corner[1] + move_y < 0) or \
                (self.view_corner[1] + move_y + self.H * self.scale_factor > 3 * self.H):
            move_y = 0

        self.view_corner = tuple(map(add, self.view_corner, (move_x, move_y)))

    def scale(self, dy, speed=2.5):
        speed = 1080 / speed
        new_scale = self.scale_factor + dy / speed
        if 0.5 < new_scale < 3:
            if new_scale > self.scale_factor:
                bottom_right_w_in_next_frame = self.view_corner[0] + self.W * new_scale
                bottom_right_h_in_next_frame = self.view_corner[1] + self.H * new_scale
                near_right_border = bottom_right_w_in_next_frame > 3 * self.W
                near_bottom_border = bottom_right_h_in_next_frame > 3 * self.H
                if near_right_border or near_bottom_border:
                    move_x = math.ceil(-bottom_right_w_in_next_frame + 3 * self.W)
                    move_y = math.ceil(-bottom_right_h_in_next_frame + 3 * self.H)
                    self.view_corner = tuple(map(add, self.view_corner, (move_x, move_y)))

            self.scale_factor = new_scale
