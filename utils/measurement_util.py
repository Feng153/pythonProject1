import math

import cv2
import numpy as np
import pyrealsense2 as rs
import torch


class MeasurementUtils(object):
    def get_3d_camera_coordinate(self, depth_pixel, depth_frame, depth_intrin):
        x = depth_pixel[0]
        y = depth_pixel[1]
        dis = depth_frame.get_distance(x, y)  # 获取该像素点对应的深度
        camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
        return dis, camera_coordinate

    '''
    两点距离
    '''

    def cal_distance(self, p1, p2):
        return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2) + math.pow((p2[2] - p1[2]), 2))

    '''
    内径测量
    '''

    def hough_detection(self, img, depth_frame, depth_intrin):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Find circles with HoughCircles
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=100, param2=10, minRadius=30,
                                   maxRadius=40)

        # Draw circles
        radius = math.inf
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for circle in circles:
                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])
                cv2.circle(img, (x, y), r, (0, 255, 0), 3)
                if (x - r) >= 1280 or (x + r) >= 1280 or y >= 720 or (x - r) <= 0 or y <= 0:
                    continue
                p1 = [x - r, y]
                p2 = [x + r, y]
                dis1, c1 = self.get_3d_camera_coordinate(p1, depth_frame, depth_intrin)
                dis2, c2 = self.get_3d_camera_coordinate(p2, depth_frame, depth_intrin)
                dist = self.cal_distance(c1, c2)
                if dist < radius:
                    radius = dist
        return radius

    '''
    矩阵中行向量两两距离
    '''

    def EuclideanDistances(self, A, B):
        BT = B.transpose()
        # vecProd = A * BT
        vecProd = np.dot(A, BT)
        # print(vecProd)
        SqA = A ** 2
        # print(SqA)
        sumSqA = np.matrix(np.sum(SqA, axis=1))
        sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))
        # print(sumSqAEx)

        SqB = B ** 2
        sumSqB = np.sum(SqB, axis=1)
        sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))
        SqED = sumSqBEx + sumSqAEx - 2 * vecProd
        SqED[SqED < 0] = 0.0
        ED = np.sqrt(SqED)
        return ED

    '''
    外径、长、宽测量
    '''

    def corner_detection(self, img, depth_frame, depth_intrin):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # harris角点检测图像需为float32
        gray = np.float32(imgray)
        dst = cv2.cornerHarris(gray, 8, 3, 0.04)
        dst = cv2.dilate(dst, None)
        ret, dst = cv2.threshold(dst, 0.005 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        # 图像连通域
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        # 迭代停止规则
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
        res = np.hstack((centroids, corners))
        res = np.int0(res)

        corner_axis = []

        for i in res:
            x1, y1, x2, y2 = i.ravel()
            point = [x1, y1]
            dis, coordinate_3d = self.get_3d_camera_coordinate(point, depth_frame, depth_intrin)
            corner_axis.append(coordinate_3d)

        corners = np.array(corner_axis)
        d = self.EuclideanDistances(corners, corners)
        d = torch.from_numpy(d)
        r1 = torch.argmax(d)
        a = r1.item() / 2
        b = 2 * a * math.cos(math.radians(30))
        return r1.item(), a, b
