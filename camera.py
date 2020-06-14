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
        shape = frame.shape
        weight, height = shape[0]/5, shape[1]/5
        resize_frame = cv2.resize(frame, (height, weight), interpolation=cv2.INTER_CUBIC)
        #resize_frame = frame
        #img = cv2.imread('dave.jpg')
        gray_frame = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_frame, 127, 255, 0)
        #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        _, contours, _= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(resize_frame, contours, -1, (0,255,0), 3)
        #cv2.imshow("gray", gray_frame)
        edges = cv2.Canny(gray_frame,50,150,apertureSize = 3)
        minLineLength = 10
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
        #print ("lines: ", lines)
        """
        try:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    cv2.line(resize_frame,(x1,y1),(x2,y2),(153,51,255),3)
        except:
            print ("there's no line")
        """
        #for x1,y1,x2,y2 in lines[0]:
        #    cv2.line(resize_frame,(x1,y1),(x2,y2),(153,51,255),2)

        cv2.imshow('line', resize_frame)
        #cv2.imwrite('houghlines5.jpg',img)
        
        """
        hsv_frame = rgbtohsv(resize_frame) # try to hsv or hsl
        result_frame = np.zeros((resize_frame.shape))
        for x in range(0, weight):
            for y in range(0, height):
                if (resize_frame[x, y, 0] > 300 or resize_frame[x, y, 0] < 60):
                    result_frame[x, y, 2] = 255
                    result_frame[x, y, 0] = result_frame[x, y, 1] = 0
                elif (resize_frame[x, y, 1] > 60 and resize_frame[x, y, 0] < 180):
                    result_frame[x, y, 1] = 255
                    result_frame[x, y, 0] = result_frame[x, y, 2] = 0
                elif (resize_frame[x, y, 0] > 180 and resize_frame[x, y, 0] < 300):
                    result_frame[x, y, 0] = 255
                    result_frame[x, y, 1] = result_frame[x, y, 2] = 0

        cv2.imshow('video', result_frame)
        
        #numpy_vertical = np.vstack((image, grey_3_channel))
        hori_together = np.hstack((resize_frame, hsv_frame, result_frame))

        #numpy_vertical_concat = np.concatenate((image, grey_3_channel), axis=0)
        hori_concat = np.concatenate((resize_frame, hsv_frame, result_frame), axis=1)
        """

        #cv2.imshow('video', hori_concat)
        if (cv2.waitKey(1) == 'q'):
            break
        #print ("shape of frame: ", frame.shape)
    camera.usb_camera.release()
    cv2.destroyAllWindows()

