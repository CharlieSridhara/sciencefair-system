import threading
import cv2
from detection.camera import CameraStream
from detection.detector import PlaqueDetector


class FluoroController:

    def __init__(self, on_pass_callback):
        self.camera = CameraStream()
        self.detector = PlaqueDetector()
        self.on_pass = on_pass_callback
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def loop(self):
        while self.running:
            frame = self.camera.get_frame()
            if frame is None:
                continue

            mask, frac = self.detector.build_red_mask(frame)
            detected, plaque_removed = self.detector.update(frac)

            if plaque_removed:
                self.on_pass()

            cv2.imshow("Live View", frame)
            cv2.imshow("Red Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break