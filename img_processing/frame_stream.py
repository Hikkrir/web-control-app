import cv2 as cv
cap = cv.VideoCapture(0, cv.CAP_DSHOW)

def get_frame():
    ret, frame = cap.read()
    if ret:
        return frame
    else:
        return False