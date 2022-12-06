import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Blue Green Orange
penColorHSV = [[73, 69, 111, 126, 183, 255],
               [46, 55, 62, 69, 133, 255],
               [8, 106, 176, 26, 206, 255]]

penColorBGR = [[255, 128, 64],
               [0, 219, 0],
               [0, 128, 255]]

drawPoints = []


def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(len(penColorHSV)):
        lower = np.array(penColorHSV[i][:3])
        upper = np.array(penColorHSV[i][3:6])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)

        penx, peny = findContour(mask)
        cv2.circle(imgContour, (penx, peny), 10, penColorBGR[i], cv2.FILLED)
        if peny != -1:
            drawPoints.append([penx, peny, i])
        # cv2.imshow('result', result)


def findContour(img):
    x, y, w, h = -1, -1, -1, -1
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.2, True)
            x, y, w, h = cv2.boundingRect(vertices)
            # cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return x, y


def draw(drawpoints):
    for point in drawpoints:
        cv2.circle(imgContour, (point[0], point[1]), 10, penColorBGR[point[2]], cv2.FILLED)


while True:
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 180)
        imgContour = frame.copy()
        # cv2.imshow('video', frame)
        findPen(frame)
        draw(drawPoints)
        cv2.imshow('contour', imgContour)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break

# def empty(v):
#     pass
#
#
# cv2.namedWindow('TrackBar')
# cv2.resizeWindow('TrackBar', 640, 320)
#
# cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty)
# cv2.createTrackbar('Hue Max', 'TrackBar', 179, 179, empty)
# cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
# cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
# cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
# cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
#
# while True:
#     h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
#     h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
#     s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
#     s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
#     v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
#     v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
#     print(h_min, h_max, s_min, s_max, v_min, v_max)
#
#     ret, img = cap.read()
#     img = cv2.flip(img, 180)
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
#     lower = np.array([h_min, s_min, v_min])
#     upper = np.array([h_max, s_max, v_max])
#
#     mask = cv2.inRange(hsv, lower, upper)
#     result = cv2.bitwise_and(img, img, mask=mask)
#
#     cv2.imshow('img', img)
#     cv2.imshow('mask', mask)
#     cv2.imshow('reslut', result)
#     cv2.waitKey(1)
