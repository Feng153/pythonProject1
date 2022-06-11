import cv2
import numpy as np


class FeatureUtils(object):

    def canny(self, img):
        canny = cv2.Canny(img, 100, 200)
        res = cv2.cvtColor(canny, cv2.COLOR_BGR2RGB)
        return res

    def sobel(self, img):
        x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)

        dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        return dst

    def laplacian(self, img):
        # out = cv2.GaussianBlur(img, (3, 3), 1.3)
        gray_lap = cv2.Laplacian(img, cv2.CV_16S, 1.3)
        dst = cv2.convertScaleAbs(gray_lap)
        return dst

    def harris(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float32(imgray)
        dst = cv2.cornerHarris(gray, 8, 3, 0.04)
        dst = cv2.dilate(dst, None)
        ret, dst = cv2.threshold(dst, 0.005 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
        res = np.hstack((centroids, corners))
        res = np.int0(res)
        for i in res:
            x1, y1, x2, y2 = i.ravel()
            # cv2.circle(img, (x1, y1), 3, 255, -1)
            cv2.circle(img, (x2, y2), 3, (0, 255, 0), -1)
        image = img[:, :, ::-1]
        image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def fast(self, img):
        image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fast = cv2.FastFeatureDetector_create()
        kp = fast.detect(image1, None)
        frame = cv2.drawKeypoints(image1, kp, None, color=(0, 255, 0))
        image = frame[:, :, ::-1]
        image = image.copy()
        return image

    def tomasi(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, 72, 0.01, 10)
        corners = np.int0(corners)
        for i in corners:
            x, y = i.ravel()
            cv2.circle(img, (x, y), 3, 255, -1)
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        image = img[:, :, ::-1]
        image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def hough_detection(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist=150, circles=None, param1=200, param2=18,
                                   maxRadius=40, minRadius=20)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(img, (x, y), r, (36, 255, 12), 3)
        image = img[:, :, ::-1]
        image = image.copy()
        return image

    def hough_detection(self, img, minr, maxr):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist=150, circles=None, param1=200, param2=18,
                                   maxRadius=maxr, minRadius=minr)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(img, (x, y), r, (36, 255, 12), 3)
        image = img[:, :, ::-1]
        image = image.copy()
        return image
