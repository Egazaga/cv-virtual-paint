import threading


class GestureLock:
    def __init__(self):
        self.gesture = "No gesture"
        self.action = "No action"
        self.pairs = {3: "Yellow", 5: "Erasing", 0: "Green", 2: "Brown", 1: "Blue", 4: "Black"}
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
