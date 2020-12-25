import threading


class GestureLock:
    def __init__(self):
        self.gesture = "No gesture"
        self.action = "No action"
        self.pen_in_frame = False
        self.pairs = {"OK": "Yellow", "Palm": "Erasing", "Fist": "Green", "Two": "Brown", "Five": "Blue"}
        self.lock = threading.Lock()

    def get_gesture(self):
        with self.lock:
            gesture = self.gesture
            action = self.action
        return gesture, action

    def set_gesture(self, gesture):
        with self.lock:
            self.gesture = gesture
            self.action = self.pairs[gesture]

    def set_pen_in_frame(self, flag):
        with self.lock:
            self.pen_in_last_frame = flag
