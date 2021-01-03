import numpy as np
import cv2


class Drawing:
    def __init__(self, W, H):
        self.x1, self.y1 = 0, 0
        self.canvas = np.zeros((int(H), int(W), 3), dtype=np.uint8)
        self.previous_action = ""

    def process_frame(self, frame, action, point, thickness):
        if point is not None:
            x2, y2 = point[0], point[1]

            # if we have same action, and coordinates of a pen from previous frame
            if action == self.previous_action and self.x1 != 0 and self.y1 != 0:
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
                elif action == "Black":
                    color = [255, 255, 255]
                self.canvas = cv2.line(self.canvas, (self.x1, self.y1), (x2, y2), color, thickness=thickness)
            self.x1, self.y1 = x2, y2
        else:
            self.x1, self.y1 = 0, 0
        self.previous_action = action

        # return cv2.add(frame, self.canvas)
        return cv2.addWeighted(frame, 0.3, self.canvas, 0.7, 0)
