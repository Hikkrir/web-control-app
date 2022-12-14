import numpy as np
import cv2 as cv

from servo_motor_handler import Control
from img_processing.frame_stream import get_frame

# #929ca5

class RoadDetection():
    def __init__(self):
        self.controller = Control()

        self.AVG_VALUE = 10
        self.Y_MIDDLE = 640
        self.CURVE_LIST = []
        # [110,240,0,400]
        # [0, 350, 0, 600]
        self.TRACKBAR_WIDTH_TOP = 110
        self.TRACKBAR_HEIGHT_TOP = 240
        self.TRACKBAR_WIDTH_BOTTOM = 0
        self.TRACKBAR_HEIGHT_BOTTOM = 400

        self.TRACKBAR_WINDOW_WIGTH = 360
        self.TRACKBAR_WINDOW_height = 360

        self.GRAY_LOWER = np.array([0, 0, 0])
        self.GRAY_UPPER = np.array([179, 19, 255])

    def thresholding_frame(self, video_frame):
        hsv = cv.cvtColor(video_frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,self.GRAY_LOWER, self.GRAY_UPPER)
        return mask

    def trackbars_values(self, frame_window_widht):
        points = np.float32([(self.TRACKBAR_WIDTH_TOP, self.TRACKBAR_HEIGHT_TOP), (frame_window_widht - self.TRACKBAR_WIDTH_TOP, self.TRACKBAR_HEIGHT_TOP),
                        (self.TRACKBAR_WIDTH_BOTTOM , self.TRACKBAR_HEIGHT_BOTTOM ), (frame_window_widht - self.TRACKBAR_WIDTH_BOTTOM, self.TRACKBAR_HEIGHT_BOTTOM)])
        return points

    def warp_img(self, frame, points, widht, height, inverse= False):
        pts1 = np.float32(points)
        pts2 = np.float32([[0, 0], [widht, 0], [0, height], [widht, height]])
        if inverse:
            matrix = cv.getPerspectiveTransform(pts2, pts1)
        else:
            matrix = cv.getPerspectiveTransform(pts1, pts2)
        warped_img = cv.warpPerspective(frame, matrix, (widht, height))
        return warped_img

    def draw_points_in_frame(self, frame, points):
        for i in range(0, 4):
            cv.circle(frame, (int(points[i][0]), int(points[i][1])), 15, (0, 0, 255), cv.FILLED)
        return frame

    def get_histogram(self, frame, min_percentage = 0.1, region= 1):
        if region == 1:
            histValues = np.sum(frame, axis=0)
        else:
            histValues = np.sum(frame[frame.shape[0]//region:,:], axis=0)
        
        max_value = np.max(histValues)
        min_value = min_percentage*max_value
        
        index_list = np.where(histValues >= min_value)
        base_point = int(np.average(index_list))
        
        img_hist = np.zeros((int(frame.shape[0]), int(frame.shape[1]), 3), np.uint8)
        for i, intensity in enumerate(histValues):
            cv.line(img_hist, (i, int(frame.shape[0])), (i, int(frame.shape[0]-intensity//255//region)), (255, 0, 255), 1)
            cv.circle(img_hist, (base_point, frame.shape[0]), 20, (0, 255, 255), cv.FILLED)
        return base_point, img_hist

    def video_stream(self):
        print("stream up")
        while True:
            input_frame_list = get_frame()
            if input_frame_list[0]:
                frame = input_frame_list[1].copy()
                hT, wT, c = frame.shape
                frame_result = input_frame_list[1].copy()

                warped_img = self.warp_img(self.thresholding_frame(frame), self.trackbars_values(frame_window_widht=wT), wT, hT)
                middle_point, _ = self.get_histogram(warped_img, min_percentage= 0.5, region= 4)
                curve_avarage_point, _ = self.get_histogram(warped_img, min_percentage= 0.9)
                curve_raw = curve_avarage_point - middle_point

                self.CURVE_LIST.append(curve_raw)
                if len(self.CURVE_LIST) > self.AVG_VALUE:
                    self.CURVE_LIST.pop(0)
                curve = int(sum(self.CURVE_LIST)/len(self.CURVE_LIST))

                warped_inverted_img = self.warp_img(warped_img, self.trackbars_values(frame_window_widht=wT), wT, hT, inverse=True)
                warped_inverted_img = cv.cvtColor(warped_inverted_img, cv.COLOR_GRAY2BGR)
                warped_inverted_img[0:hT // 3, 0:wT] = 0, 0, 0
                img_lane_color = np.zeros_like(frame)
                img_lane_color[:] = 0, 255, 0
                img_lane_color = cv.bitwise_and(warped_inverted_img, img_lane_color)
                frame_result = cv.addWeighted(frame_result, 1, img_lane_color, 1,0)

                cv.putText(frame_result,str(curve),(wT//2-80,85),cv.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
                cv.line(frame_result, (wT//2, self.Y_MIDDLE), (wT//2 + (curve * 3), self.Y_MIDDLE), (255, 0, 255), 5)
                cv.line(frame_result, ((wT // 2 + (curve * 3)), self.Y_MIDDLE - 25), (wT // 2 + (curve * 3), self.Y_MIDDLE + 25), (0, 255, 0), 5)

                for i in range(-30, 30):
                    width = wT // 20
                    cv.line(frame_result, (width * i + int(curve//50), self.Y_MIDDLE - 10),
                                (width * i + int(curve//50), self.Y_MIDDLE + 10), (0, 0, 255), 2)
                _, buffer = cv.imencode('.jpg', frame_result)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def automode(self):
        print("automode available\nSPEED: 80")
        while True:
            input_frame_list = get_frame()
            if input_frame_list[0]:
                frame_for_stream = input_frame_list[1].copy()
                hT, wT, c = frame_for_stream.shape
                
                warped_img = self.warp_img(self.thresholding_frame(frame_for_stream), self.trackbars_values(frame_window_widht=wT), wT, hT)
                middle_point, _ = self.get_histogram(warped_img, min_percentage= 0.7, region= 4)
                curve_avarage_point, _ = self.get_histogram(warped_img, min_percentage= 0.9)
                curve_raw = curve_avarage_point - middle_point

                self.CURVE_LIST.append(curve_raw)
                if len(self.CURVE_LIST) > self.AVG_VALUE:
                    self.CURVE_LIST.pop(0)
                curve = int(sum(self.CURVE_LIST)/len(self.CURVE_LIST))
                with open('check.txt', 'r') as file:
                    automode = file.readline()
                    if automode == "true":
                        sensitivity = 5
                        speed = 80
                        max_angle_val = 50
                        min_angle_val = 25
                        default_angle_value = 110
                        
                        self.controller.move_forward(speed)
                        if abs(curve) > sensitivity:
                            if min_angle_val < curve < max_angle_val:
                                angle = default_angle_value + curve
                                self.controller.change_angle_servo(angle)
                            if 0 > curve :
                                angle = default_angle_value + curve
                                self.controller.change_angle_servo(angle)

if __name__ == "__main__":
    RoadDetection().video_processing(automode= True)