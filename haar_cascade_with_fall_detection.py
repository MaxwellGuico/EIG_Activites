from __future__ import print_function
import cv2 as cv
import argparse
j=0
def detectAndDisplay(frame):
    global j
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    fgmask = fgbg.apply(frame_gray) #Apply the fgbg to gray pic

    #Find contours
    contours, _ = cv.findContours(fgmask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # source img, contour retrivial mode, contour approximation method
    if contours:
        # List to hold all areas
        areas = []

        for contour in contours:
            ar = cv.contourArea(contour) # Returns area of coutours
            areas.append(ar) #Adds ar to areas

        max_area = max(areas, default = 0) #Compares values to find maximum area

        max_area_index = areas.index(max_area) # Finds the index of this area and passes it to max_area_index
    
        cnt = contours[max_area_index] # finds the point of countour that has the highest area

        M = cv.moments(cnt) #Used to find the center of blob

        x, y, w, h = cv.boundingRect(cnt) #draws a bouding box at the point of countour that has the highest area

        cv.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0) # draw contours

        if h < w:
            j += 1 # if width of bounding box's width is higher than height, add one to counter j

        if j > 10:
            logging.info('FALL')
           # print("FALL")
           # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) # draw red rectangle when j is more than 10, known as falling

        if h > w:
            j = 0 # reset j to 0
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # draw green rectangle when height  more than width
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    cv.imshow('Capture - Face detection', frame)
    

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

fgbg = cv.createBackgroundSubtractorMOG2() # Help to remove background
while True:
    ret, frame = cap.read()
    
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break