import cv2 as cv
import datetime

cap = cv.VideoCapture(0)

start_img = cap.read()[1]
out = cv.VideoWriter("outvideo.avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (start_img.shape[1], start_img.shape[0]))

sTime = datetime.datetime.utcnow().timestamp() * 1000
while True:
    ret, camera_img = cap.read()

    cv.imshow("Preview", camera_img)
    out.write(camera_img)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

print((datetime.datetime.utcnow().timestamp() * 1000) - sTime)
out.release()
cap.release()
cv.destroyAllWindows()