import cv2
import numpy as np
from collections import deque

MIN_RED_DOM_RATIO = 1.55
MIN_RED_INTENSITY = 90
ON_FRACTION = 0.012
OFF_FRACTION = 0.006
EMA_ALPHA = 0.6
VOTE_WINDOW = 4


class PlaqueDetector:

    def __init__(self):
        self.ema = 0
        self.state = False
        self.votes = deque(maxlen=VOTE_WINDOW)

    def build_red_mask(self, frame):
        frame = cv2.GaussianBlur(frame, (5,5), 0)

        b = frame[:,:,0].astype(np.float32)
        g = frame[:,:,1].astype(np.float32)
        r = frame[:,:,2].astype(np.float32)

        red_ratio = r / (g + b + 1)
        mask = (
            (red_ratio > MIN_RED_DOM_RATIO) &
            (r > MIN_RED_INTENSITY)
        )

        mask = mask.astype(np.uint8) * 255
        red_fraction = np.count_nonzero(mask) / mask.size

        return mask, red_fraction

    def update(self, fraction):
        self.ema = (1 - EMA_ALPHA)*self.ema + EMA_ALPHA*fraction

        if self.state:
            frame_on = self.ema >= OFF_FRACTION
        else:
            frame_on = self.ema >= ON_FRACTION

        self.votes.append(1 if frame_on else 0)
        new_state = sum(self.votes)/len(self.votes) >= 0.5

        previous = self.state
        self.state = new_state

        plaque_removed = previous and not new_state

        return self.state, plaque_removed