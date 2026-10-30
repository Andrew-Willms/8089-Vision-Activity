import cv2
import math


def nothing(x):
    pass



def contour_center(contour) -> tuple[int, int]:

    moments: dict[str, float] = cv2.moments(contour)

    if moments["m00"] == 0:
        return 0, 0

    return int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])



def diameter_of_circular_contour(contour) -> int:
    return 2 * math.sqrt(cv2.contourArea(contour) / math.pi)