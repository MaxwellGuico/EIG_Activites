#Based on Zed code - Person Fall detection using raspberry pi camera and opencv lib. Link: https://www.youtube.com/watch?v=eXMYZedp0Uo

import cv2
import time

fitToEllipse = False
video_name = ''
cap = cv2.VideoCapture(0)
time.sleep(2)

fgbg = cv2.createBackgroundSubtractorMOG2() # Help to remove background
j = 0

while(1):
    ret, frame = cap.read() #ret in bool, frame in array
    
    #Convert each frame to gray scale and subtract the background

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converts to gray
    fgmask = fgbg.apply(gray) #Apply the fgbg to gray pic

    #Find contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # source img, contour retrivial mode, contour approximation method
    print(_)
    # Returns points of contours and 
    '''
    Different retrivial mode:
    RETR_LIST - Parents and Childs are equal, just contours
    RETR_EXTERNAL - Only the oldest/Top of the hierachy, dont care about others
    RETR_CCOMP -
    RETR_TREE - All contours and creates full hierachy list
    '''
    if contours:
        # List to hold all areas
        areas = []

        for contour in contours:
            ar = cv2.contourArea(contour) # Returns area of coutours
            areas.append(ar) #Adds ar to areas

        max_area = max(areas, default = 0) #Compares values to find maximum area

        max_area_index = areas.index(max_area) # Finds the index of this area and passes it to max_area_index
    
        cnt = contours[max_area_index] # finds the 

        M = cv2.moments(cnt)

        x, y, w, h = cv2.boundingRect(cnt)

        cv2.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0)

        if h < w:
            j += 1

        if j > 10:
           # print("FALL")
           # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        if h > w:
            j = 0 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


        cv2.imshow('video', frame)

        if cv2.waitKey(33) == 27:
         break
        
cap.release()
cv2.destroyAllWindows()
