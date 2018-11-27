import cv2 as cv
import datetime

cap = cv.VideoCapture(0)

start_img = cap.read()[1]

while True:
    ret, camera_img = cap.read()
    cv.medianBlur(camera_img, 5, camera_img)
    camera_img = cv.cvtColor(camera_img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(camera_img, 150, 200)
    cv.imshow("Preview", edges)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
