import cv2 as cv
cap = cv.VideoCapture(0)

def get_frame():
    ret, frame = cap.read()
    return [ret, frame]