# car.py
import time
import numpy as np
import cv2

class camera:
    def __init__(self):
        try:
            self.usb_camera = cv2.VideoCapture(1)
        except:
            try:
                self.usb_camera = cv2.VideoCapture(0)
            except:
                print ("there's no camera")
        time.sleep(0.1)

    def capture(self):
        while True:
            ret, frame = self.usb_camera.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            cv2.imshow('Video', frame)

        self.usb_camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    #car = car()
    #car.capture()
    camera = camera()
    camera.capture()