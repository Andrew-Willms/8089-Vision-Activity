import cv2
import math
import numpy

import utilities



# sudo apt update
# sudo apt install python3-pip -y
# sudo apt install python3-opencv -y
# 45 vertical, 60 horizontal


# Camera Resolution
HORIZONTAL_RESOLUTION: int = 640
VERTICAL_RESOLUTION: int = 480
HALF_HORIZONTAL_RESOLUTION: int = HORIZONTAL_RESOLUTION / 2
HALF_VERTICAL_RESOLUTION: int = VERTICAL_RESOLUTION / 2

# Camera Specs
F_X: float = 594.777
F_Y: float = 594.449
C_X: float = 323.116
C_Y: float = 237.647

K1: float = 0.026486
K2: float = 0.11972
P1: float = -0.0051909
P2: float = -0.00071865
K3: float = -1.0536

CAMERA_MATRIX = numpy.array([
    [ F_X,  0,   C_X ],
    [ 0,    F_Y, C_Y ],
    [ 0,    0,   1   ]
], dtype=numpy.float64)

DISTORTION_COEFFICIENTS = numpy.array([
    K1, K2, P1, P2, K3
], dtype=numpy.float64)

# Ball Specs
BALL_DIAMETER: float = 0.066 # m

# Center Indicator Parameters
CIRCLE_COLOR: tuple[int, int, int] = (0, 0, 255)
CIRCLE_RADIUS: int = 3
CIRCLE_THICKNESS: int = -1

# Text Parameters
TEXT_START_COORDINATES: tuple[int, int] = (math.floor(HORIZONTAL_RESOLUTION * 0.05), math.floor(VERTICAL_RESOLUTION * 0.95))
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE: float = HORIZONTAL_RESOLUTION / 1280
TEXT_COLOR: tuple[int, int, int] = (0, 0, 255)
TEXT_THICKNESS: int = 1
TEXT_LINE_TYPE = cv2.LINE_AA
TEXT_IS_BOTTOM_LEFT_ORIGIN: bool = False



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



def get_ball_camera_coords_and_area(mask: numpy.ndarray) -> tuple[float, float, float] | None:

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None

    largest_contour = max(contours, key = cv2.contourArea)
    center = utilities.contour_center(largest_contour)
    area: float = cv2.contourArea(largest_contour)

    points = numpy.array([[[center[0], center[1]]]], dtype=numpy.float64)
    undistorted_points = cv2.undistortPoints(
        points,
        CAMERA_MATRIX,
        DISTORTION_COEFFICIENTS,
        P=CAMERA_MATRIX
    )

    return (float(undistorted_points[0, 0, 0]), float(undistorted_points[0, 0, 1]), area)



def get_ball_angle(center: tuple[float, float]) -> tuple[float, float] | None:

    x: float = float(numpy.arctan((center[0] - C_X) / F_X))

    y: float = -float(numpy.arctan((center[1] - C_Y) / F_Y))

    return (x, y)



def get_ball_position(ball_pixel_area: float) -> float:

    distance: float = BALL_DIAMETER * 0.5 * (F_X + F_Y) / ball_pixel_area



    return 0.0



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

        center: tuple[float, float]
        area: float
        (center, area) | None = get_ball_camera_coords_and_area(mask)

        print(area)

        if (center != None):

            cv2.circle(colorized_mask, (int(center[0]), int(center[1])), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            camera_angle: tuple[float, float] = get_ball_angle(center)

            horizontal_angle_degrees: float = (camera_angle[0] / math.pi * 180)
            vertical_angle_degrees: float = (camera_angle[1] / math.pi * 180)
            angle_text: str = f"horizontal angle: {horizontal_angle_degrees:.0f}, vertical angle: {vertical_angle_degrees:.0f}"
            cv2.putText(colorized_mask, angle_text, TEXT_START_COORDINATES, FONT, FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)

            print(f"horizontal angle: {horizontal_angle_degrees:4.0f}, vertical angle {vertical_angle_degrees:4.0f}")

        else:
            print("Ball not found.")
            cv2.putText(colorized_mask, "No ball found", TEXT_START_COORDINATES, FONT, FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)

        cv2.imshow("Red", numpy.hstack((frame_resized, colorized_mask)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()