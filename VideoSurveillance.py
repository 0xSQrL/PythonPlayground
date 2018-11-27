import cv2 as cv
import datetime
from collections import deque
import numpy
import os


def force_folder(folder_name):
    if not os.path.exists(os.path.join(os.getcwd(), folder_name)):
        os.mkdir(os.path.join(os.getcwd(), folder_name))


def save_image_buffer(buffer, filename, fps):

    first_frame = buffer[0]
    print("Creating file " + filename + ".avi of length " + str(len(buffer) / fps) + "s")
    out = cv.VideoWriter(filename + ".avi", cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                         (first_frame.shape[1], first_frame.shape[0]))
    while len(buffer) > 0:
        out.write(buffer.popleft())
    out.release()


cap = cv.VideoCapture(0)

frames_per_second = 10
ms_per_frame = int(1000 / frames_per_second)
buffer_seconds = 2
buffer_frames = frames_per_second * buffer_seconds
buffer_frames_push = 0
start_img = cap.read()[1]
img_buffer = deque()
img_buffer.append(start_img)
tolerance = start_img.shape[1] * start_img.shape[0] * 7

sTime = datetime.datetime.utcnow().timestamp() * 1000

while True:
    ret, camera_img = cap.read()

    if len(img_buffer) > 0:
        diff = numpy.zeros(camera_img.shape, camera_img.dtype)
        cv.absdiff(camera_img, img_buffer[-1], diff)
        value = numpy.sum(diff)
        if value > tolerance:
            print(str(value) + " " + str(tolerance))
            buffer_frames_push = buffer_frames + len(img_buffer)

    img_buffer.append(camera_img)

    if len(img_buffer) >= buffer_frames + buffer_frames_push:
        if buffer_frames_push != 0:
            buffer_frames_push = 0
            force_folder("motions")
            unique_filename = "motions/motion" + str(int(datetime.datetime.utcnow().timestamp() * 1000))
            save_image_buffer(img_buffer, unique_filename, frames_per_second)
        else:
            img_buffer.popleft()

    cv.imshow("Preview", camera_img)

    key = cv.waitKey(ms_per_frame) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

