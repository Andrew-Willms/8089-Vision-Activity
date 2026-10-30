import cv2
import math
import numpy

import utilities



# sudo apt update
# sudo apt install python3-pip -y
# sudo apt install python3-opencv -y
# 45 vertical, 60 horizontal


# Resolution
HORIZONTAL_RESOLUTION: int = 640
VERTICAL_RESOLUTION: int = 480
HALF_HORIZONTAL_RESOLUTION: int = HORIZONTAL_RESOLUTION / 2
HALF_VERTICAL_RESOLUTION: int = VERTICAL_RESOLUTION / 2

# FOV
HORIZONTAL_FOV_DEGREES: float = 45
VERTICAL_FOV_DEGREES: float = 30
HORIZONTAL_FOV: float = HORIZONTAL_FOV_DEGREES / 180 * math.pi
VERTICAL_FOV: float = VERTICAL_FOV_DEGREES / 180 * math.pi
HALF_HORIZONTAL_FOV: float = HORIZONTAL_FOV / 2.0
HALF_VERTICAL_FOV: float = VERTICAL_FOV / 2.0

# Center Indicator Parameters
CIRCLE_COLOR: tuple[int, int, int] = (0, 0, 255)
CIRCLE_RADIUS: int = 3
CIRCLE_THICKNESS: int = -1

# Text Parameters
TEXT_START_COORDINATES: tuple[int, int] = (VERTICAL_RESOLUTION * 0.9, HORIZONTAL_RESOLUTION * 0.05)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE: float = 1.0
TEXT_COLOR: tuple[int, int, int] = (0, 0, 255)
TEXT_THICKNESS: int = 2
TEXT_LINE_TYPE = cv2.LINE_AA



# Initialize GUI
cv2.namedWindow("Red")
# cv2.createTrackbar("min hue", "Red", 0, 179, utilities.nothing)
# cv2.createTrackbar("max hue", "Red", 179, 179, utilities.nothing)
# cv2.createTrackbar("min saturation", "Red", 0, 255, utilities.nothing)
# cv2.createTrackbar("max saturation", "Red", 255, 255, utilities.nothing)
# cv2.createTrackbar("min value", "Red", 0, 255, utilities.nothing)
# cv2.createTrackbar("max value", "Red", 255, 255, utilities.nothing)
cv2.createTrackbar("min hue", "Red", 125, 179, utilities.nothing)
cv2.createTrackbar("max hue", "Red", 138, 179, utilities.nothing)
cv2.createTrackbar("min saturation", "Red", 155, 255, utilities.nothing)
cv2.createTrackbar("max saturation", "Red", 229, 255, utilities.nothing)
cv2.createTrackbar("min value", "Red", 140, 255, utilities.nothing)
cv2.createTrackbar("max value", "Red", 255, 255, utilities.nothing)



def create_mask(frame: numpy.ndarray) -> numpy.ndarray:

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
    return cv2.inRange(frame_hsv, lower_bound, upper_bound)



def get_ball_camera_coords(mask: numpy.ndarray) -> tuple[float, float] | None:

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("Red ball not found.")
        return None

    largest_contour = max(contours, key = cv2.contourArea)
    center = utilities.contour_center(largest_contour)

    return center



def get_ball_angle(center: tuple[float, float]) -> tuple[float, float] | None:

    horizontal_pixels_from_center: float = center[0] - HALF_HORIZONTAL_RESOLUTION # positive is to the right
    distance_to_image_plane: float = HALF_HORIZONTAL_RESOLUTION / math.tan(HALF_HORIZONTAL_FOV) # tan=O/A -> A=O/tan
    theta_horizontal: float = math.atan2(horizontal_pixels_from_center, distance_to_image_plane)

    vertical_pixels_from_center: float = -center[1] + HALF_VERTICAL_RESOLUTION # positive is towards the top
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

        frame_resized = cv2.resize(cv2.flip(frame, 1), (HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION))

        mask = create_mask(frame)
        colorized_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        center: tuple[int, int] | None = get_ball_camera_coords(mask)

        if (center != None):

            cv2.circle(colorized_mask, center, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            camera_angle: tuple[int, int] = get_ball_angle(center)

            horizontal_angle_degrees: float = (camera_angle[0] / math.pi * 180)
            vertical_angle_degrees: float = (camera_angle[1] / math.pi * 180)
            angle_text: str = f"horizontal angle: {horizontal_angle_degrees:4.0f}, vertical angle {vertical_angle_degrees:4.0f}"
            cv2.putText(colorized_mask, TEXT_START_COORDINATES, FONT, FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE)

        cv2.imshow("Red", numpy.hstack((frame_resized, colorized_mask)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()