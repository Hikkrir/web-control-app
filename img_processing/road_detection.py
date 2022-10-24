import numpy as np
import cv2 as cv

# #929ca5

class RoadDetection():
    def __init__(self) -> None:
        # self.cap = cv.VideoCapture("D:\Captures\example.mp4")
        # self.cap = cv.VideoCapture(0)

        self.AVG_VALUE = 10
        self.Y_MIDDLE = 450
        self.CURVE_LIST = []

        # [0, 350, 0, 600]
        self.TRACKBAR_WIDTH_TOP = 0
        self.TRACKBAR_HEIGHT_TOP = 350
        self.TRACKBAR_WIDTH_BOTTOM = 0
        self.TRACKBAR_HEIGHT_BOTTOM = 600


        self.FRAME_WINDOW_WIDHT = 1280
        self.FRAME_WINDOW_HEIGHT = 720
        self.TRACKBAR_WINDOW_WIGTH = 360
        self.TRACKBAR_WINDOW_height = 360

        self.GRAY_LOWER = np.array([0, 0, 0])
        self.GRAY_UPPER = np.array([179, 19, 255])

    def thresholding_frame(self, video_frame):
        hsv = cv.cvtColor(video_frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,self.GRAY_LOWER, self.GRAY_UPPER)
        return mask

    def trackbars_values(self):
        points = np.float32([(self.TRACKBAR_WIDTH_TOP, self.TRACKBAR_HEIGHT_TOP), (self.FRAME_WINDOW_WIDHT - self.TRACKBAR_WIDTH_TOP, self.TRACKBAR_HEIGHT_TOP),
                        (self.TRACKBAR_WIDTH_BOTTOM , self.TRACKBAR_HEIGHT_BOTTOM ), (self.FRAME_WINDOW_WIDHT - self.TRACKBAR_WIDTH_BOTTOM, self.TRACKBAR_HEIGHT_BOTTOM)])
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

    def get_histogram(self, frame, display=False, min_percentage = 0.1, region= 1):
        histValues = np.sum(frame, axis=0)
        max_value = np.max(histValues)
        min_value = min_percentage*max_value
        
        index_list = np.where(histValues >= min_value)
        base_point = int(np.average(index_list))
        
        if region == 1:
            histValues = np.sum(frame, axis=0)
        else:
            histValues = np.sum(frame[frame.shape[0]//region:,:], axis=0)
        
        if display:
            img_hist = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
            for i, intensity in enumerate(histValues):
                cv.line(img_hist, (i, frame.shape[0]), (i, frame.shape[0]-intensity//255//region), (255, 0, 255), 1)
                cv.circle(img_hist, (base_point, frame.shape[0]), 20, (0, 255, 255), cv.FILLED)
            return base_point, img_hist
        return base_point

    def get_frame_with_curve_result(self, frame= None, return_curve= False):
        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            hT, wT, c = frame.shape
            if ret:
                frame_result = frame
                warped_img = RoadDetection().warp_img(RoadDetection().thresholding_frame(frame), RoadDetection().trackbars_values(), wT, hT)
                middle_point, img_histogram = RoadDetection().get_histogram(warped_img, display= True, min_percentage= 0.5, region= 4)
                curve_avarage_point, img_histogram = RoadDetection().get_histogram(warped_img, display= True, min_percentage= 0.9)
                curve_raw = curve_avarage_point - middle_point

                self.CURVE_LIST.append(curve_raw)
                if len(self.CURVE_LIST) > self.AVG_VALUE:
                    self.CURVE_LIST.pop(0)
                curve = int(sum(self.CURVE_LIST)/len(self.CURVE_LIST))

                if return_curve:
                    return curve

                warped_inverted_img = RoadDetection().warp_img(warped_img, RoadDetection().trackbars_values(), wT, hT, inverse=True)
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

    def curve_val_generator(self, frame):
        curve_value = RoadDetection().get_frame_with_curve_result(frame, return_curve= True)
        print(curve_value)

    def get_complete_img_stream(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                frame_with_hist_and_curve = RoadDetection().get_frame_with_curve_result(frame)
                cv.imshow('Resutlt', frame_with_hist_and_curve)
            else:
                self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            if cv.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    RoadDetection().get_complete_img_stream()