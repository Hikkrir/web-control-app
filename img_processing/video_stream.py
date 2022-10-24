import cv2 as cv

def video_generator():
    # cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap = cv.VideoCapture(0)
    while True:
        yield cap