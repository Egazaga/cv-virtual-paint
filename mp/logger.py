import pandas as pd


class Logger:
    def __init__(self, drawing, motion_analyser):
        columns = ["n_fingers", "hand_pos_x", "hand_pos_y", "pen_pos_x", "pen_pos_y", "pen_area", "view_corner_x", "view_corner_y",
                   "scale_factor", "ma_dx", "ma_dy"]
        self.memory = pd.DataFrame(columns=columns)
        self.drawing = drawing
        self.ma = motion_analyser

    def log(self, n_fingers, hand_pos, pen_pos, pen_area):
        if hand_pos is None:
            info = [n_fingers, None, None, pen_pos[0],  pen_pos[1], pen_area,
                    self.drawing.view_corner[0], self.drawing.view_corner[1],
                    self.drawing.scale_factor, self.ma.total_dx, self.ma.total_dy]
        else:
            info = [n_fingers, hand_pos[0], hand_pos[1], pen_pos[0],  pen_pos[1], pen_area,
                    self.drawing.view_corner[0], self.drawing.view_corner[1],
                    self.drawing.scale_factor, self.ma.total_dx, self.ma.total_dy]
        self.memory.loc[len(self.memory)] = info

    def save_to_disk(self, path="tests/system/info.csv"):
        self.memory.to_csv(path, index=False)
