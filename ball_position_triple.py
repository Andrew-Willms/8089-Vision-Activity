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
BALL_DIAMETER: float = 0.066 # meters
PIXEL_AREA_AT_1M: int = 1111

# Center Indicator Parameters
RED_CIRCLE_COLOR: tuple[int, int, int] = (0, 0, 255)
GREEN_CIRCLE_COLOR: tuple[int, int, int] = (0, 255, 0)
BLUE_CIRCLE_COLOR: tuple[int, int, int] = (255, 0, 0)
CIRCLE_RADIUS: int = 3
CIRCLE_THICKNESS: int = -1

# Text Parameters
BOTTOM_TEXT_START_COORDINATES: tuple[int, int] = (math.floor(HORIZONTAL_RESOLUTION * 0.05), math.floor(VERTICAL_RESOLUTION * 0.95))
RED_TEXT_START_COORDINATES: tuple[int, int] = (math.floor(HORIZONTAL_RESOLUTION * 0.05), math.floor(VERTICAL_RESOLUTION * 0.85))
GREEN_TEXT_START_COORDINATES: tuple[int, int] = (math.floor(HORIZONTAL_RESOLUTION * 0.05), math.floor(VERTICAL_RESOLUTION * 0.90))
BLUE_TEXT_START_COORDINATES: tuple[int, int] = (math.floor(HORIZONTAL_RESOLUTION * 0.05), math.floor(VERTICAL_RESOLUTION * 0.95))
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE: float = HORIZONTAL_RESOLUTION / 1280
RED_TEXT_COLOR: tuple[int, int, int] = (0, 0, 255)
GREEN_TEXT_COLOR: tuple[int, int, int] = (0, 255, 0)
BLUE_TEXT_COLOR: tuple[int, int, int] = (255, 0, 0)
TEXT_THICKNESS: int = 1
TEXT_LINE_TYPE = cv2.LINE_AA
TEXT_IS_BOTTOM_LEFT_ORIGIN: bool = False

# Triangle
SIDE_LENGTH: float = 0.20 # meters
VERTICES = numpy.array([
        [  0,                SIDE_LENGTH / numpy.sqrt(3),       0 ],
        [ -SIDE_LENGTH / 2, -SIDE_LENGTH / (2 * numpy.sqrt(3)), 0 ],
        [  SIDE_LENGTH / 2, -SIDE_LENGTH / (2 * numpy.sqrt(3)), 0 ]
    ], dtype=numpy.float64)



# Initialize GUI
#cv2.namedWindow("Window")
cv2.namedWindow("Red")
cv2.namedWindow("Green")
cv2.namedWindow("Blue")
cv2.setWindowProperty("Red", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("Green", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("Blue", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.createTrackbar("R min hue", "Red", 0, 179, utilities.nothing)
cv2.createTrackbar("R max hue", "Red", 179, 179, utilities.nothing)
cv2.createTrackbar("R min saturation", "Red", 0, 255, utilities.nothing)
cv2.createTrackbar("R max saturation", "Red", 255, 255, utilities.nothing)
cv2.createTrackbar("R min value", "Red", 0, 255, utilities.nothing)
cv2.createTrackbar("R max value", "Red", 255, 255, utilities.nothing)
# cv2.createTrackbar("R min hue", "Red", 125, 179, utilities.nothing)
# cv2.createTrackbar("R max hue", "Red", 138, 179, utilities.nothing)
# cv2.createTrackbar("R min saturation", "Red", 155, 255, utilities.nothing)
# cv2.createTrackbar("R max saturation", "Red", 229, 255, utilities.nothing)
# cv2.createTrackbar("R min value", "Red", 140, 255, utilities.nothing)
# cv2.createTrackbar("R max value", "Red", 255, 255, utilities.nothing)

cv2.createTrackbar("G min hue", "Green", 0, 179, utilities.nothing)
cv2.createTrackbar("G max hue", "Green", 179, 179, utilities.nothing)
cv2.createTrackbar("G min saturation", "Green", 0, 255, utilities.nothing)
cv2.createTrackbar("G max saturation", "Green", 255, 255, utilities.nothing)
cv2.createTrackbar("G min value", "Green", 0, 255, utilities.nothing)
cv2.createTrackbar("G max value", "Green", 255, 255, utilities.nothing)
# cv2.createTrackbar("G min hue", "Green", 33, 179, utilities.nothing)
# cv2.createTrackbar("G max hue", "Green", 74, 179, utilities.nothing)
# cv2.createTrackbar("G min saturation", "Green", 52, 255, utilities.nothing)
# cv2.createTrackbar("G max saturation", "Green", 197, 255, utilities.nothing)
# cv2.createTrackbar("G min value", "Green", 48, 255, utilities.nothing)
# cv2.createTrackbar("G max value", "Green", 255, 255, utilities.nothing)

cv2.createTrackbar("B min hue", "Blue", 0, 179, utilities.nothing)
cv2.createTrackbar("B max hue", "Blue", 179, 179, utilities.nothing)
cv2.createTrackbar("B min saturation", "Blue", 0, 255, utilities.nothing)
cv2.createTrackbar("B max saturation", "Blue", 255, 255, utilities.nothing)
cv2.createTrackbar("B min value", "Blue", 0, 255, utilities.nothing)
cv2.createTrackbar("B max value", "Blue", 255, 255, utilities.nothing)
# cv2.createTrackbar("B min hue", "Blue", 6, 179, utilities.nothing)
# cv2.createTrackbar("B max hue", "Blue", 25, 179, utilities.nothing)
# cv2.createTrackbar("B min saturation", "Blue", 115, 255, utilities.nothing)
# cv2.createTrackbar("B max saturation", "Blue", 253, 255, utilities.nothing)
# cv2.createTrackbar("B min value", "Blue", 0, 88, utilities.nothing)
# cv2.createTrackbar("B max value", "Blue", 255, 255, utilities.nothing)



def create_masks(frame: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:

    r_lower_bound = numpy.array([0, 0, 0])
    r_upper_bound = numpy.array([179, 255, 255])
    r_lower_bound[0] = cv2.getTrackbarPos("R min hue", "Red")
    r_upper_bound[0] = cv2.getTrackbarPos("R max hue", "Red")
    r_lower_bound[1] = cv2.getTrackbarPos("R min saturation", "Red")
    r_upper_bound[1] = cv2.getTrackbarPos("R max saturation", "Red")
    r_lower_bound[2] = cv2.getTrackbarPos("R min value", "Red")
    r_upper_bound[2] = cv2.getTrackbarPos("R max value", "Red")\

    g_lower_bound = numpy.array([0, 0, 0])
    g_upper_bound = numpy.array([179, 255, 255])
    g_lower_bound[0] = cv2.getTrackbarPos("G min hue", "Green")
    g_upper_bound[0] = cv2.getTrackbarPos("G max hue", "Green")
    g_lower_bound[1] = cv2.getTrackbarPos("G min saturation", "Green")
    g_upper_bound[1] = cv2.getTrackbarPos("G max saturation", "Green")
    g_lower_bound[2] = cv2.getTrackbarPos("G min value", "Green")
    g_upper_bound[2] = cv2.getTrackbarPos("G max value", "Green")

    b_lower_bound = numpy.array([0, 0, 0])
    b_upper_bound = numpy.array([179, 255, 255])
    b_lower_bound[0] = cv2.getTrackbarPos("B min hue", "Blue")
    b_upper_bound[0] = cv2.getTrackbarPos("B max hue", "Blue")
    b_lower_bound[1] = cv2.getTrackbarPos("B min saturation", "Blue")
    b_upper_bound[1] = cv2.getTrackbarPos("B max saturation", "Blue")
    b_lower_bound[2] = cv2.getTrackbarPos("B min value", "Blue")
    b_upper_bound[2] = cv2.getTrackbarPos("B max value", "Blue")

    # The actual resolution also happens to be 640x480 on the Acer Spin 713...
    # So I don't need to resize the image, but this makes the program more portable.
    frame_resized = cv2.resize(cv2.flip(frame, 1), (HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION))
    frame_hsv = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2HSV)

    return (
        cv2.inRange(frame_hsv, r_lower_bound, r_upper_bound),
        cv2.inRange(frame_hsv, g_lower_bound, g_upper_bound),
        cv2.inRange(frame_hsv, b_lower_bound, b_upper_bound)
    )



def get_ball_camera_coords(mask: numpy.ndarray) -> tuple[float, float] | None:

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None

    largest_contour = max(contours, key = cv2.contourArea)
    center = utilities.contour_center(largest_contour)

    points = numpy.array([[[center[0], center[1]]]], dtype=numpy.float64)
    undistorted_points = cv2.undistortPoints(
        points,
        CAMERA_MATRIX,
        DISTORTION_COEFFICIENTS,
        P=CAMERA_MATRIX
    )

    return (float(undistorted_points[0, 0, 0]), float(undistorted_points[0, 0, 1]))



def get_ball_position(red_image_coords: tuple[float, float], green_image_coords: tuple[float, float], blue_image_coords: tuple[float, float]) -> tuple[float, float, float] | None:

    image_points = numpy.array([
        red_image_coords,
        green_image_coords,
        blue_image_coords
    ], dtype=numpy.float64)

    success, rotation_vector, translation_vector = cv2.solvePnP(
        VERTICES,
        image_points,
        CAMERA_MATRIX,
        DISTORTION_COEFFICIENTS,
        flags=cv2.SOLVEPNP_SQPNP
    )

    if not success:
        return None

    return (float(translation_vector[0]), float(-translation_vector[1]), float(translation_vector[2]))



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
        frame_copy = frame_resized.copy()

        masks: tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray] = create_masks(frame)
        red_mask_colorized: numpy.ndarray = cv2.cvtColor(masks[0], cv2.COLOR_GRAY2BGR)
        green_mask_colorized: numpy.ndarray = cv2.cvtColor(masks[1], cv2.COLOR_GRAY2BGR)
        blue_mask_colorized: numpy.ndarray = cv2.cvtColor(masks[2], cv2.COLOR_GRAY2BGR)

        red_center: tuple[float, float] | None = get_ball_camera_coords(masks[0])
        green_center: tuple[float, float] | None = get_ball_camera_coords(masks[1])
        blue_center: tuple[float, float] | None = get_ball_camera_coords(masks[2])

        ###################
        ####    Red    ####
        ###################

        if red_center != None:

            cv2.circle(red_mask_colorized, (int(red_center[0]), int(red_center[1])), CIRCLE_RADIUS, RED_CIRCLE_COLOR, CIRCLE_THICKNESS)
            cv2.circle(frame_copy, (int(red_center[0]), int(red_center[1])), CIRCLE_RADIUS, RED_CIRCLE_COLOR, CIRCLE_THICKNESS)

        else:
            print("Red ball not found.")
            cv2.putText(red_mask_colorized, "No ball found", BOTTOM_TEXT_START_COORDINATES, FONT, FONT_SCALE, RED_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)
            cv2.putText(frame_copy, "No ball found", RED_TEXT_START_COORDINATES, FONT, FONT_SCALE, RED_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)

        cv2.imshow("Red", numpy.hstack((frame_resized, red_mask_colorized)))

        #####################
        ####    Green    ####
        #####################

        if green_center != None:

            cv2.circle(green_mask_colorized, (int(green_center[0]), int(green_center[1])), CIRCLE_RADIUS, GREEN_CIRCLE_COLOR, CIRCLE_THICKNESS)
            cv2.circle(frame_copy, (int(green_center[0]), int(green_center[1])), CIRCLE_RADIUS, GREEN_CIRCLE_COLOR, CIRCLE_THICKNESS)

        else:
            print("Green ball not found.")
            cv2.putText(green_mask_colorized, "No ball found", BOTTOM_TEXT_START_COORDINATES, FONT, FONT_SCALE, GREEN_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)
            cv2.putText(frame_copy, "No ball found", GREEN_TEXT_START_COORDINATES, FONT, FONT_SCALE, GREEN_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)

        cv2.imshow("Green", numpy.hstack((frame_resized, green_mask_colorized)))

        ####################
        ####    Blue    ####
        ####################

        if blue_center != None:

            cv2.circle(blue_mask_colorized, (int(blue_center[0]), int(blue_center[1])), CIRCLE_RADIUS, BLUE_CIRCLE_COLOR, CIRCLE_THICKNESS)
            cv2.circle(frame_copy, (int(blue_center[0]), int(blue_center[1])), CIRCLE_RADIUS, BLUE_CIRCLE_COLOR, CIRCLE_THICKNESS)

        else:
            print("Blue ball not found.")
            cv2.putText(blue_mask_colorized, "No ball found", BOTTOM_TEXT_START_COORDINATES, FONT, FONT_SCALE, BLUE_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)
            cv2.putText(frame_copy, "No ball found", BOTTOM_TEXT_START_COORDINATES, FONT, FONT_SCALE, BLUE_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)

        cv2.imshow("Blue", numpy.hstack((frame_resized, blue_mask_colorized)))

        ########################

        if red_center != None and green_center != None and blue_center != None and not (red_center == green_center and green_center == blue_center):

            ball_position: tuple[float, float, float] = get_ball_position(red_center, green_center, blue_center)

            position_text: str = f"x: {ball_position[0]:.2f}, y: {ball_position[1]:.2f}, z: {ball_position[2]:.2f}"
            cv2.putText(frame_copy, position_text, BOTTOM_TEXT_START_COORDINATES, FONT, FONT_SCALE, RED_TEXT_COLOR, TEXT_THICKNESS, TEXT_LINE_TYPE, TEXT_IS_BOTTOM_LEFT_ORIGIN)
            print(f"x: {ball_position[0]:2.2f}, y: {ball_position[1]:2.2f}, z: {ball_position[2]:.2f}")

        else:
            print("Jig not found")


        cv2.imshow("Main", cv2.resize(frame_copy, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()