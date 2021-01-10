import numpy as np
import cv2 as cv

img = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2() # Help BG
j = 0
while(1):
    ret,frame = img.read()
    
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    print(type(fgbg))
    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # source img, contour retrivial mode, contour approximation method
    '''
    if contours:
        # List to hold all areas
        areas = []

        for contour in contours:
            ar = cv.contourArea(contour)
            areas.append(ar)

        max_area = max(areas, default = 0)

        max_area_index = areas.index(max_area)
    
        cnt = contours[max_area_index]

        M = cv.moments(cnt)

        x, y, w, h = cv.boundingRect(cnt)

        cv.drawContours(gray, [cnt], 0, (255,255,255), 3, maxLevel = 0)
        if h < w:
            j += 1

        if j > 10:
           # print("FALL")
           # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
            cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        if h > w:
            j = 0 
            cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    '''
    cv.imshow('image',gray)
    if cv.waitKey(33) & 0xFF == 27:
        break
cv.destroyAllWindows()