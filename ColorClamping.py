import cv2 as cv
import numpy

class ColorBound:
    min_value = 0
    max_value = 256

    def set_max_value(self, value):
        self.max_value = value

    def set_min_value(self, value):
        self.min_value = value


class TrichromaticBound:
    red = ColorBound()
    green = ColorBound()
    blue = ColorBound()

    def set_color(self, r, g, b, tolerance):
        self.red.min_value = r - tolerance
        self.red.max_value = r + tolerance
        self.green.min_value = g - tolerance
        self.green.max_value = g + tolerance
        self.blue.min_value = b - tolerance
        self.blue.max_value = b + tolerance


def display_settings_window(trichroma):
    cv.namedWindow("Tools")
    min_val = 0
    max_val = 256
    cv.createTrackbar("Min Red",    "Tools",   min_val, max_val,   trichroma.red.set_min_value)
    cv.createTrackbar("Max Red",    "Tools",   max_val, max_val,   trichroma.red.set_max_value)
    cv.createTrackbar("Min Green",  "Tools", min_val, max_val,   trichroma.green.set_min_value)
    cv.createTrackbar("Max Green",  "Tools", max_val, max_val,   trichroma.green.set_max_value)
    cv.createTrackbar("Min Blue",   "Tools",  min_val, max_val,   trichroma.blue.set_min_value)
    cv.createTrackbar("Max Blue",   "Tools",  max_val, max_val,   trichroma.blue.set_max_value)


def update_settings_window(trichroma):
    cv.setTrackbarPos("Min Red", "Tools", trichroma.red.min_value)
    cv.setTrackbarPos("Max Red", "Tools", trichroma.red.max_value)
    cv.setTrackbarPos("Min Green", "Tools", trichroma.green.min_value)
    cv.setTrackbarPos("Max Green", "Tools", trichroma.green.max_value)
    cv.setTrackbarPos("Min Blue", "Tools", trichroma.blue.min_value)
    cv.setTrackbarPos("Max Blue", "Tools", trichroma.blue.max_value)


def filter_image_to_bound(color_frame, color_bound):
    zeros = numpy.zeros(color_frame.shape, color_frame.dtype)
    if color_bound.min_value == 0:
        cv.threshold(color_frame, 1, 255, cv.THRESH_BINARY_INV, zeros)
        color_frame = cv.bitwise_or(zeros, color_frame)
    cv.threshold(color_frame, color_bound.min_value, 0, cv.THRESH_TOZERO, color_frame)
    cv.threshold(color_frame, color_bound.max_value, 0, cv.THRESH_TOZERO_INV, color_frame)
    cv.threshold(color_frame, 0, 0xFF, cv.THRESH_BINARY, color_frame)
    return color_frame

