import cv2 as cv
cap = cv.VideoCapture(0, cv.CAP_DSHOW)

def get_frame():
    _, frame = cap.read()
    return frame