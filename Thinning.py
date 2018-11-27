import cv2 as cv
import datetime
import numpy

cap = cv.VideoCapture(0)

start_img = cap.read()[1]


def skeletonize(mat):
    eroded = mat.copy()
    skeleton = numpy.zeros(mat.shape, mat.dtype)
    opened = numpy.zeros(mat.shape, mat.dtype)
    while numpy.sum(eroded) != 0:
        a = eroded.copy()
        cv.erode(a, (9, 9), eroded)
        cv.dilate(eroded, (9, 9), opened)
        dif = numpy.subtract(a, opened)
        skeleton = numpy.add(skeleton, dif)
    return skeleton

while True:
    ret, camera_img = cap.read()
    cv.medianBlur(camera_img, 5, camera_img)
    camera_img = cv.cvtColor(camera_img, cv.COLOR_BGR2GRAY)
    cv.threshold(camera_img, 120, 0, cv.THRESH_TOZERO, camera_img)

    cv.imshow("Preview", camera_img)
    cv.imshow("Skeleton", skeletonize(camera_img))

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
