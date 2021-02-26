from dataclasses import dataclass


@dataclass
class Directions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class MotionAnalyser:
    def __init__(self, cam_width, cam_height, drawing):
        self.min_length_of_move_x = int(cam_width * 0.4)
        self.min_length_of_move_y = int(cam_height * 0.4)
        self.ex_pos = (cam_width / 2, cam_height / 2)
        self.ex_gesture = None
        self.total_dx = 0
        self.total_dy = 0
        self.drawing = drawing

    def analyse(self, pos, gesture):
        if gesture is None:
            self.ex_pos = 0, 0
            self.ex_gesture = None
            return
        elif gesture != self.ex_gesture:
            self.ex_pos = pos
            self.ex_gesture = gesture
            self.total_dx = 0
            self.total_dy = 0
            return

        dx = pos[0] - self.ex_pos[0]
        dy = pos[1] - self.ex_pos[1]
        self.ex_pos = pos
        self.total_dx += dx
        self.total_dy += dy

        if gesture == 5:
            self.drawing.move(dx, dy)
        elif gesture == 0:
            self.drawing.scale(dy)
