from mp.main_cam_loop import main_cam


class TestDrawingAfterMovingOrScaling:
    def a(self):
        main_cam(phone_cam=False, imgs_paths=["tests/images/hand_0.jpeg", "tests/images/hand_1.jpeg"])
        assert True
