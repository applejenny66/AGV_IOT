# car.py
# sudo ps aux | grep python | awk '{print $2}' | xargs kill -9


import time
import numpy as np
import cv2

class camera:
    def __init__(self):
        try:
            self.usb_camera = cv2.VideoCapture(0)
        except:
            try:
                self.usb_camera = cv2.VideoCapture(1)
            except:
                print ("there's no camera")
        time.sleep(0.1)

def rgbtohsv(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return (hsv_frame)

def rgbtohsl(frame):
    hsl_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    return (hsl_frame)

def test_color((r, g, b)):
    test_im = np.zeros((10, 30, 3))
    print (type(test_im))
    #change_im = np.zeros((10, 10))
    for i in range(0, 10):
        for j in range(0, 10):
            test_im[i, j, 0], test_im[i, j, 1], test_im[i, j, 2] = 0, 0, 255
    for i in range(0, 10):
        for j in range(10, 20):
            test_im[i, j, 0], test_im[i, j, 1], test_im[i, j, 2] = 0, 255, 0
    for i in range(0, 10):
        for j in range(20, 30):
            test_im[i, j, 0], test_im[i, j, 1], test_im[i, j, 2] = 255, 0, 0        
    cv2.imwrite('test_im.png', test_im)
    test_im = test_im.astype(np.uint8)
    change_im = cv2.cvtColor(test_im, cv2.COLOR_BGR2HSV)
    cv2.imwrite('changed_im.png', change_im)
    print ("red hsv: ", change_im[5, 5])
    print ("green hsv: ", change_im[5, 15])
    print ("blue hsv: ", change_im[5, 25])


if __name__ == "__main__":
    #car = car()
    #car.capture()
    test_color((0, 255, 0))
    camera = camera()
    while True:
        ret, frame = camera.usb_camera.read() # array
        frame = rgbtohsv(frame) # try to hsv or hsl
        shape = frame.shape
        weight, height = shape[0]/10, shape[1]/10
        resize_frame = cv2.resize(frame, (height, weight), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('video', resize_frame)
        if (cv2.waitKey(1) == 'q'):
            break
        #print ("shape of frame: ", frame.shape)
    camera.usb_camera.release()
    cv2.destroyAllWindows()

    #camera.capture()
    #time.sleep(5)
    #stop_camera()