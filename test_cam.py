import numpy as np
import cv2
import time
cap = cv2.VideoCapture(1)



while(True):
    h_list = []
    s_list = []
    v_list = []
    # Capture frame-by-frame
    ret, frame = cap.read()
    gus = cv2.GaussianBlur(frame, (5,5), 0)
    hsv = cv2.cvtColor(gus, cv2.COLOR_BGR2HSV)

    shape = hsv.shape
    """
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            tmp_color = hsv[x, y]
            tmp_h = tmp_color[0]
            tmp_s = tmp_color[1]
            tmp_v = tmp_color[2]
            if (tmp_h not in h_list):
                h_list.append(tmp_h)
                s_list.append(tmp_s)
                v_list.append(tmp_v)
    """
    #print ("h: ", h_list)
    #print ("s: ", s_list)
    #print ("v: ", v_list)
    time.sleep(2)

    new_shape = (shape[1] // 3, shape[0] // 3)
    resized = cv2.resize(hsv, new_shape)
    for x in range(0, new_shape[1]):
        for y in range(0, new_shape[0]):
            if (resized[x, y, 0] > 70 and resized[x, y, 0] < 320):
                pass
            else:
                resized[x, y, 0] = resized[x, y, 1] = resized[x, y, 2] = 0
    
    for x in range(0, new_shape[1]):
        for y in range(0, new_shape[0]):
            tmp_color = resized[x, y]
            tmp_h = tmp_color[0]
            tmp_s = tmp_color[1]
            tmp_v = tmp_color[2]
            if (tmp_h not in h_list):
                h_list.append(tmp_h)
                s_list.append(tmp_s)
                v_list.append(tmp_v)
    print ("h: ", h_list)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()