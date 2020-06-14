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
    #test_color((0, 255, 0))
    camera = camera()
    while True:
        ret, frame = camera.usb_camera.read() # array
        # resize
        shape = frame.shape
        weight, height = shape[0]/10, shape[1]/10
        resize_frame = cv2.resize(frame, (height, weight), interpolation=cv2.INTER_CUBIC)
        gray_frame = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
        
        # fond contours
        ret, thresh = cv2.threshold(gray_frame, 127, 255, 0)
        _, contours, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        #cv2.drawContours(resize_frame, contours, -1, (0,255,0), 2)
        #cv2.imshow("gray", gray_frame)
        
        

        # find lines(edges)
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

        #cv2.imshow('line', resize_frame)
        #cv2.imwrite('houghlines5.jpg',img)

        Z = resize_frame.reshape((-1,3))
        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 12
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        k_img = res.reshape((resize_frame.shape))

        #cv2.imshow('res2',k_img)

        
        hsv_frame = rgbtohsl(k_img) # try hsl
        cv2.imshow('k_img', hsv_frame)
        result_frame = np.zeros((resize_frame.shape))
        tmp_r = 0
        r_count = 0
        r_x_list = []
        r_y_list = []
        tmp_g = 0
        g_count = 0
        g_x_list = []
        g_y_list = []
        tmp_b = 0
        b_count = 0
        b_x_list = []
        b_y_list = []
        #cv2.imshow('hsv', hsv_frame)
        for x in range(0, weight):
            for y in range(0, height):
                if (hsv_frame[x, y, 0] > 90 and hsv_frame[x, y, 0] < 150):
                    tmp_g += hsv_frame[x, y, 0]
                    b_count += 1
        if (b_count != 0):
            tmp_g = int(tmp_g / b_count)
            #result_frame[x, y, 0] = result_frame[x, y, 1] = result_frame[x, y, 2] = 255
        for x in range(0, weight):
            for y in range(0, height):
                if (hsv_frame[x, y, 0] > tmp_g and hsv_frame[x, y, 0] < 150):
                    result_frame[x, y, 0] = result_frame[x, y, 1] = result_frame[x, y, 2] = 255
        cv2.imshow('green', result_frame)
        """
        for x in range(0, weight):
            for y in range(0, height):
                if (resize_frame[x, y, 0] > 320 or resize_frame[x, y, 0] < 40):
                    if (resize_frame[x, y, 0] > 300):
                        resize_frame[x, y, 0] = 300-resize_frame[x, y, 0]
                    tmp_r += resize_frame[x, y, 0]
                    r_count += 1
                    #result_frame[x, y, 2] = 255
                    #result_frame[x, y, 0] = result_frame[x, y, 1] = 0
                elif (resize_frame[x, y, 0] > 80 and resize_frame[x, y, 0] < 160):
                    tmp_g += resize_frame[x, y, 0]
                    g_count += 1
                    #result_frame[x, y, 1] = 255
                    #result_frame[x, y, 0] = result_frame[x, y, 2] = 0
                elif (resize_frame[x, y, 0] > 200 and resize_frame[x, y, 0] < 280):
                    tmp_b += resize_frame[x, y, 0]
                    b_count += 1
                    #result_frame[x, y, 0] = 255
                    #result_frame[x, y, 1] = result_frame[x, y, 2] = 0
        if (r_count != 0):
            print ("r: ", r_count)
            tmp_r = int(tmp_r / r_count)
        if (g_count != 0):
            print ("g: ", g_count)
            tmp_g = int(tmp_g / g_count)
        if (b_count != 0):
            tmp_b = int(tmp_b / b_count)
        for x in range(0, weight):
            for y in range(0, height):
                if (resize_frame[x, y, 0] < tmp_b and resize_frame[x, y, 0] > 180):
                    resize_frame[x, y, 0] = resize_frame[x, y, 1] = resize_frame[x, y, 2] = 0
                elif (resize_frame[x, y, 0] < tmp_g and resize_frame[x, y, 0] > 60):
                    resize_frame[x, y, 0] = resize_frame[x, y, 1] = resize_frame[x, y, 2] = 0
                elif (resize_frame[x, y, 0] < tmp_r and resize_frame[x, y, 0] > -60):
                    resize_frame[x, y, 0] = resize_frame[x, y, 1] = resize_frame[x, y, 2] = 0
        """
        #cv2.imshow('video', resize_frame)
        
        #numpy_vertical = np.vstack((image, grey_3_channel))
        #hori_together = np.hstack((resize_frame, hsv_frame, result_frame))

        #numpy_vertical_concat = np.concatenate((image, grey_3_channel), axis=0)
        #hori_concat = np.concatenate((resize_frame, hsv_frame, result_frame), axis=1)
        
        
        #cv2.imshow('video', hori_concat)
        if (cv2.waitKey(1) == 'q'):
            break
        #print ("shape of frame: ", frame.shape)
    camera.usb_camera.release()
    cv2.destroyAllWindows()

