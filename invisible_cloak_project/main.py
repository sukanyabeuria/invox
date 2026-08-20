import cv2
import numpy as np
import time

# ---------- STEP 1: Open webcam ----------
cap = cv2.VideoCapture(0)
time.sleep(2)  # let the camera warm up

# ---------- STEP 2: Capture background ----------
# IMPORTANT: Step OUT of frame while this runs (about 2-3 seconds)
background = None
for i in range(60):
    ret, frame = cap.read()
    if ret:
        background = frame

if background is None:
    print("Failed to capture background. Check your webcam.")
    cap.release()
    exit()

background = np.flip(background, axis=1)  # mirror, like a selfie cam
print("Background captured. Step into frame with your cloak now!")

# ---------- STEP 3: Your calibrated HSV values ----------
# From your calibration: H 160-179, S 50-255, V 0-255
# Red wraps around the hue circle, so we also add the 0-10 range
# to catch the full red color, not just the upper half.

lower_red1 = np.array([160, 130, 60])
upper_red1 = np.array([179, 255, 255])

lower_red2 = np.array([0, 130, 60])
upper_red2 = np.array([10, 255, 255])

kernel = np.ones((5, 5), np.uint8)

# ---------- STEP 4: Main loop ----------
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)  # mirror to match background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create mask for both red ranges and combine
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Clean the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)

    mask_inv = cv2.bitwise_not(mask)

    # Cloak area -> background pixels
    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    # Everything else -> current frame pixels
    non_cloak_area = cv2.bitwise_and(img, img, mask=mask_inv)

    # Combine both
    final_output = cv2.addWeighted(cloak_area, 1, non_cloak_area, 1, 0)

    cv2.imshow("Invisible Cloak", final_output)

    # Press 'q' to quit, press 'b' to re-capture background
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('b'):
        print("Re-capturing background... step out of frame!")
        time.sleep(1)
        for i in range(60):
            ret, frame = cap.read()
            if ret:
                background = frame
        background = np.flip(background, axis=1)
        print("Background updated!")

cap.release()
cv2.destroyAllWindows()