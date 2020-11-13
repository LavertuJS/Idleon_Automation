"""
TODO:
    - Add a check for the yellow bar instead of green.
    - Replace the 2 point check by a block check.
    - Make it easier to specify the target area.
    - Ensure the check doesn't fail if outside the border.
    - Make the template matching more discriminatory to avoid false positives.
    - Add a bitmask to template matching to ignore pixels outside the leaf.
    - Add an activate/deactivate key.
    - Reformat this whole thing into a class.
    - Make a nice UI.
"""
import numpy as np
import cv2
import mouse
import mss
import time

DEBUG = True

detection_threshold = 0.34
monitor = {'top': 0, 'left': 0, 'width': 1000, 'height': 1000}
target_offset_ver = 42  # Pixels
target_offset_hor = 10  # Pixels
target_color = [20, 138, 38]  # Green bar (BGR)

leaf_icon = cv2.imread("ChoppingAssets.bmp")
leaf_icon_depth, leaf_icon_width, leaf_icon_height = leaf_icon.shape[::-1]

with mss.mss() as sct:

    while True:

        # Get screen capture.
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Find the leaf icon on screen.
        res = cv2.matchTemplate(img, leaf_icon, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If a leaf is detected.
        if max_val > detection_threshold:

            # Check if the leaf is above the green/yellow bar.
            if np.all(img[max_loc[1] + target_offset_ver, max_loc[0] + target_offset_hor] == target_color) and \
                    np.all(img[max_loc[1] + target_offset_ver, max_loc[0] - target_offset_hor] == target_color):
                print("Leaf is above green bar.")
                mouse.click("left")
                time.sleep(0.5)
            else:
                print("Leaf not in correct position.")

            if DEBUG:
                img[max_loc[1] + target_offset_ver, max_loc[0] + target_offset_hor] = [0, 255, 255]
                cv2.circle(img, (max_loc[0] + target_offset_hor, max_loc[1] + target_offset_ver), 2, 255, 1)
                cv2.circle(img, (max_loc[0] - target_offset_hor, max_loc[1] + target_offset_ver), 2, 255, 1)

        else:
            print("No leaf detected.")

        if DEBUG:
            # Add a rectangle around the leaf on the image for debug purposes.
            top_left = max_loc
            bottom_right = (top_left[0] + leaf_icon_width, top_left[1] + leaf_icon_height)
            cv2.rectangle(img, top_left, bottom_right, 255, 2)
            cv2.imshow("derp", img)

        # Exit on 'q' press.
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
