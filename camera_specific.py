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

def test_color(r, g, b):
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


def find_green(weight, height, r, g, b):
    pass

if __name__ == "__main__":
    #car = car()
    #car.capture()
    #test_color((0, 255, 0))
    camera = camera()
    index_desigated = 2 #0 = b, 1 = g, 2 = r
    kernel = np.ones((4,4),np.float32)/16
    while True:
        ret, frame = camera.usb_camera.read() # array
        # resize
        
        shape = frame.shape
        weight, height = shape[0]//10, shape[1]//10
        resize_frame = cv2.resize(frame, (height, weight), interpolation=cv2.INTER_CUBIC)
        resize_frame = cv2.filter2D(resize_frame,-1,kernel)
        gray_frame = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
        Z = resize_frame.reshape((-1,3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 12
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        k_img = res.reshape((resize_frame.shape))

        hsv_frame = rgbtohsl(k_img) # try hsl
        cv2.imshow('k_img', hsv_frame)

        Z = hsv_frame.reshape((-1,3))
        Z = np.float32(Z)
        K = 2
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        k_hsv = res.reshape((hsv_frame.shape))
        cv2.imshow("k_hsv", k_hsv)
        h_list = []
        s_list = []
        l_list = []
        for x in range(0, weight):
            for y in range(0, height):
                tmp_h = k_hsv[x, y, 0]
                tmp_s = k_hsv[x, y, 1]
                tmp_l = k_hsv[x, y, 2]
                if (tmp_h not in h_list):
                    h_list.append(tmp_h)
                    s_list.append(tmp_s)
                    l_list.append(tmp_l)
                else:
                    if (tmp_s not in s_list):
                        h_list.append(tmp_h)
                        s_list.append(tmp_s)
                        l_list.append(tmp_l)
                    else:
                        if (tmp_l not in l_list):
                            h_list.append(tmp_h)
                            s_list.append(tmp_s)
                            l_list.append(tmp_l)
        result_frame = np.zeros((resize_frame.shape))

        count_1 = 0
        count_2 = 0
        for x in range(0, weight):
            for y in range(0, height):
                if (k_hsv[x, y, 0] == h_list[0] and k_hsv[x, y, 1] == s_list[0]\
                    and k_hsv[x, y, 2] == l_list[0]):
                    count_1 += 1
                else:
                    count_2 += 1
        
        x_list = []
        y_list = []
        if (count_1 > count_2):
            for x in range(0, weight):
                for y in range(0, height):
                    if (k_hsv[x, y, 0] == h_list[1] and k_hsv[x, y, 1] == s_list[1]\
                        and k_hsv[x, y, 2] == l_list[1]):
                        tmp_color = (resize_frame[x, y, 0], resize_frame[x, y, 1], \
                            resize_frame[x, y, 2])
                        max_color = max(tmp_color)
                        max_index = tmp_color.index(max_color)
                        # blue
                        if (max_index == index_desigated):
                            if (max_index == 0):
                                result_frame[x, y, 1] = result_frame[x, y, 2] = 255
                                result_frame[x, y, 0] = 255
                                x_list.append(x)
                                y_list.append(y)
                            
                            elif (max_index == 1):
                                result_frame[x, y, 0] = result_frame[x, y, 2] = 255
                                result_frame[x, y, 1] = 255
                                x_list.append(x)
                                y_list.append(y)
                            else:
                                result_frame[x, y, 0] = result_frame[x, y, 1] = 255
                                result_frame[x, y, 2] = 255
                                x_list.append(x)
                                y_list.append(y)
                        else:
                            result_frame[x, y, 0] = result_frame[x, y, 1] = result_frame[x, y, 2] = 0
        else:
            for x in range(0, weight):
                for y in range(0, height):
                    if (k_hsv[x, y, 0] == h_list[0] and k_hsv[x, y, 1] == s_list[0]\
                        and k_hsv[x, y, 2] == l_list[0]):
                        tmp_color = (resize_frame[x, y, 0], resize_frame[x, y, 1], \
                            resize_frame[x, y, 2])
                        max_color = max(tmp_color)
                        max_index = tmp_color.index(max_color)
                        if (max_index == index_desigated):
                            if (max_index == 0):
                                result_frame[x, y, 1] = result_frame[x, y, 2] = 255
                                result_frame[x, y, 0] = 255
                                x_list.append(x)
                                y_list.append(y)
                            
                            elif (max_index == 1):
                                result_frame[x, y, 0] = result_frame[x, y, 2] = 255
                                result_frame[x, y, 1] = 255
                                x_list.append(x)
                                y_list.append(y)
                            else:
                                result_frame[x, y, 0] = result_frame[x, y, 1] = 255
                                result_frame[x, y, 2] = 255
                                x_list.append(x)
                                y_list.append(y)
                        else:
                            result_frame[x, y, 0] = result_frame[x, y, 1] = result_frame[x, y, 2] = 0
        avg_x = sum(x_list) / len(x_list)
        avg_y = sum(y_list) / len(y_list)
        mean_weight = int(weight / 2) #|v
        mean_height = int(height / 2) #->

        if abs(avg_x-mean_weight) < 5:
            if abs(avg_y-mean_height) < 5:
                print ("ok")
            else:
                print ("x")
        else:
            print ("x")

        #cv2.imshow('result', result_frame)
        
        if (cv2.waitKey(1) == 'q'):
            break
    camera.usb_camera.release()
    cv2.destroyAllWindows()

