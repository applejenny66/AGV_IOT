import numpy as np
import cv2

sdThresh = 2

font = cv2.FONT_HERSHEY_SIMPLEX
#TODO: Face Detection 1

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


cv2.namedWindow('frame')
cv2.namedWindow('dist')
#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(1)
_, frame1 = cap.read()
_, frame2 = cap.read()


alpha = 0
beta = (1.0 - alpha)


while (True):
    _, frame3 = cap.read()
    hsv = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)
    hsv2 = hsv.copy()
    shape = hsv.shape
    #print ("shape: ", shape)
    cv2.imshow('hsv', hsv)
    rows, cols, _ = np.shape(frame3)
    dist = distMap(frame1, frame3)
    #print ("shape dist: ", dist.shape)
    frame1 = frame2
    frame2 = frame3
    mod = cv2.GaussianBlur(dist, (9,9), 0)
    _, thresh = cv2.threshold(mod, 100, 255, 0)
    _, stDev = cv2.meanStdDev(mod)

    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            if (mod[x, y] >= 200):
                hsv2[x, y, 0] = hsv2[x, y, 1] = hsv2[x, y, 2] = 0

    cv2.imshow('hsv2', hsv2)
    #dst = cv2.addWeighted(hsv, alpha, dist, beta, 0.0)

    #cv2.imshow('dst', dst)

    #cv2.imshow('dist', dist)
    cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
    if stDev > sdThresh:
        print("Motion detected.. Do something!!!")

    cv2.imshow('frame', frame3)
    if cv2.waitKey(1) & 0xFF == 27:
        break



cap.release()
cv2.destroyAllWindows()


