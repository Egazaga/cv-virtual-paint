from mp.drawing import Drawing


class TestDrawingMove:
    def setup(self):
        self.width = 1920
        self.height = 1080
        self.drawing = Drawing(self.width, self.height)

    def test_normal_move(self):
        oldpos = self.drawing.view_corner
        dx = -10
        dy = -10
        speed = 2.5
        self.drawing.move(dx, dy, speed)
        newpos = self.drawing.view_corner
        assert oldpos[0] - speed * dx == newpos[0]
        assert oldpos[1] - speed * dy == newpos[1]

    def test_move_top_left(self):
        self.drawing.view_corner = 0, 0
        oldpos = self.drawing.view_corner
        dx = 10
        dy = 10
        speed = 2.5
        self.drawing.move(dx, dy, speed)
        newpos = self.drawing.view_corner
        assert newpos[0] == oldpos[0]
        assert newpos[1] == oldpos[1]

    def test_move_top_right(self):
        self.drawing.view_corner = 3 * self.drawing.W, 0
        oldpos = self.drawing.view_corner
        dx = -10
        dy = -10
        speed = 2.5
        self.drawing.move(dx, dy, speed)
        newpos = self.drawing.view_corner
        assert newpos[0] == oldpos[0]
        assert newpos[1] == oldpos[1] - speed * dy

    def test_move_bottom_left(self):
        self.drawing.view_corner = 0, 3 * self.drawing.H
        oldpos = self.drawing.view_corner
        dx = -10
        dy = -10
        speed = 2.5
        self.drawing.move(dx, dy, speed)
        newpos = self.drawing.view_corner
        assert newpos[0] == oldpos[0] - speed * dy
        assert newpos[1] == oldpos[1]

    def test_move_bottom_right(self):
        self.drawing.view_corner = 3 * self.drawing.W, 3 * self.drawing.H
        oldpos = self.drawing.view_corner
        dx = -10
        dy = -10
        speed = 2.5
        self.drawing.move(dx, dy, speed)
        newpos = self.drawing.view_corner
        assert newpos[0] == oldpos[0]
        assert newpos[1] == oldpos[1]
