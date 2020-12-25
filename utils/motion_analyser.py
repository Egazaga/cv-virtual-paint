from dataclasses import dataclass


@dataclass
class Directions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class MotionAnalyser:
    def __init__(self, cam_width, cam_height):
        self.min_length_of_move_x = int(cam_width * 0.4)
        self.min_length_of_move_y = int(cam_height * 0.4)
        self.ex_center = (cam_width / 2, cam_height / 2)
        self.ex_gesture = None
        self.total_dx = 0
        self.total_dy = 0

    def analyse(self, center, gesture):
        if gesture is None:
            return None

        dx = center[0] - self.ex_center[0]
        dy = center[1] - self.ex_center[1]
        self.ex_center = center

        flag = False
        if abs(self.total_dx + dx) < abs(self.total_dx):  # if changed direction
            self.total_dx = 0
            flag = True
        if abs(self.total_dy + dy) < abs(self.total_dy):  # if changed direction
            self.total_dy = 0
            flag = True
        if gesture != self.ex_gesture:  # if detected new gesture
            self.ex_gesture = gesture
            flag = True
        if flag:
            return None

        self.total_dx += dx
        self.total_dy += dy
        direction = None
        if self.total_dx > self.min_length_of_move_x:
            direction = Directions.RIGHT
        if self.total_dx < -self.min_length_of_move_x:
            direction = Directions.LEFT
        if self.total_dy > self.min_length_of_move_y:
            direction = Directions.DOWN
        if self.total_dy < -self.min_length_of_move_y:
            direction = Directions.UP
        if direction is not None:
            self.total_dx = 0
            self.total_dy = 0
        return direction
