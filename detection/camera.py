import serial
import struct
import numpy as np
import cv2

PORT = "/dev/cu.usbmodem1101"
BAUD = 921600
MAX_FRAME_BYTES = 900000


class CameraStream:

    def __init__(self):
        self.ser = serial.Serial(PORT, BAUD, timeout=2)

    def read_exact(self, size):
        data = b''
        while len(data) < size:
            chunk = self.ser.read(size - len(data))
            if not chunk:
                return None
            data += chunk
        return data

    def get_frame(self):
        self.ser.write(b'c')

        size_bytes = self.read_exact(4)
        if not size_bytes:
            return None

        frame_size = struct.unpack('<I', size_bytes)[0]
        if frame_size <= 0 or frame_size > MAX_FRAME_BYTES:
            return None

        jpeg = self.read_exact(frame_size)
        if not jpeg:
            return None

        return cv2.imdecode(
            np.frombuffer(jpeg, dtype=np.uint8),
            cv2.IMREAD_COLOR
        )