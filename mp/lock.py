# import threading
#
#
# class GestureLock:
#     def __init__(self):
#         self.info = (None, None, None)
#         self.lock = threading.Lock()
#
#     def get_gesture(self):
#         with self.lock:
#             info = self.info
#         return info
#
#     def set_gesture(self, n_fingers_l, pointy_r, thickness):
#         with self.lock:
#             if n_fingers_l is not None:
#                 self.info = (n_fingers_l, pointy_r, thickness)
#             else:  # keep previous gesture if none
#                 self.info = (self.info[0], pointy_r, thickness)
