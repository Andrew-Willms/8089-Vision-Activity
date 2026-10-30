import cv2
import math
import numpy

import utilities



# sudo apt update
# sudo apt install python3-pip -y
# sudo apt install python3-opencv -y
# 45 vertical, 60 horizontal



HORIZONTAL_RESOLUTION: int = 640
VERTICAL_RESOLUTION: int = 480
HALF_HORIZONTAL_RESOLUTION: int = HORIZONTAL_RESOLUTION / 2
HALF_VERTICAL_RESOLUTION: int = VERTICAL_RESOLUTION / 2

HORIZONTAL_FOV_DEGREES: float = 45
VERTICAL_FOV_DEGREES: float = 30
HORIZONTAL_FOV: float = HORIZONTAL_FOV_DEGREES / 180 * math.pi
VERTICAL_FOV: float = VERTICAL_FOV_DEGREES / 180 * math.pi
HALF_HORIZONTAL_FOV: float = HORIZONTAL_FOV / 2.0
HALF_VERTICAL_FOV: float = VERTICAL_FOV / 2.0



# Initialize GUI
cv2.namedWindow("Red")
cv2.createTrackbar("min hue", "Red", 0, 179, utilities.nothing)
cv2.createTrackbar("max hue", "Red", 179, 179, utilities.nothing)
cv2.createTrackbar("min saturation", "Red", 0, 255, utilities.nothing)
cv2.createTrackbar("max saturation", "Red", 255, 255, utilities.nothing)
cv2.createTrackbar("min value", "Red", 0, 255, utilities.nothing)
cv2.createTrackbar("max value", "Red", 255, 255, utilities.nothing)



def get_red_ball_camera_coords(frame: numpy.ndarray) -> tuple[float, float] | None:

    lower_bound = numpy.array([0, 0, 0])
    upper_bound = numpy.array([179, 255, 255])
    lower_bound[0] = cv2.getTrackbarPos("min hue", "Red")
    upper_bound[0] = cv2.getTrackbarPos("max hue", "Red")
    lower_bound[1] = cv2.getTrackbarPos("min saturation", "Red")
    upper_bound[1] = cv2.getTrackbarPos("max saturation", "Red")
    lower_bound[2] = cv2.getTrackbarPos("min value", "Red")
    upper_bound[2] = cv2.getTrackbarPos("max value", "Red")

    # The actual resolution also happens to be 640x480 on the Acer Spin 713...
    # So I don't need to resize the image, but this makes the program more portable.
    frame_resized = cv2.resize(cv2.flip(frame, 1), (HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION))
    frame_hsv = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(frame_hsv, lower_bound, upper_bound)
    colorized_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    cv2.imshow("Red", numpy.hstack((frame_resized, colorized_mask)))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("Red ball not found.")
        return None

    largest_contour = max(contours, key = cv2.contourArea)
    center = utilities.contour_center(largest_contour)

    return (center[0], center[1])



def get_red_ball_angle(frame: numpy.ndarray) -> tuple[float, float] | None:

    result = get_red_ball_camera_coords(frame)

    if result == None:
        return None

    x: int
    y: int
    x, y = result

    horizontal_pixels_from_center: float = x - HALF_HORIZONTAL_RESOLUTION # positive is to the right
    distance_to_image_plane: float = HALF_HORIZONTAL_RESOLUTION / math.tan(HALF_HORIZONTAL_FOV) # tan=O/A -> A=O/tan
    theta_horizontal: float = math.atan2(horizontal_pixels_from_center, distance_to_image_plane)

    vertical_pixels_from_center: float = -y + HALF_VERTICAL_RESOLUTION # positive is towards the top
    distance_to_image_plane: float = HALF_VERTICAL_RESOLUTION / math.tan(HALF_VERTICAL_FOV) # tan=O/A -> A=O/tan
    theta_vertical: float = math.atan2(vertical_pixels_from_center, distance_to_image_plane)

    print(f"horizontal angle: {(theta_horizontal / math.pi * 180):4.0f}, vertical angle {(theta_vertical / math.pi * 180):4.0f}")

    return (theta_horizontal, theta_vertical)



def main():

    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Error: Could not open the webcam.")
        exit()

    print("Press 'q' to exit the program.")

    while True:

        success: bool
        frame: numpy.ndarray
        success, frame = webcam.read()
        
        if not success:
            print("Error: Can't receive frame. Exiting...")
            break

        output = get_red_ball_angle(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()