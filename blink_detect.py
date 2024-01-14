import numpy as np
import cv2
import time

# import call.py make_emergency_call function
from call import make_emergency_call

blink_time_value = 0.4

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# Starting the video capture
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Failed to open camera")
    exit()

ret, img = cap.read()

eye_open = True
prev_eye_open = True
is_blinking = False
blink_count = 0
last_blink_time = 0

start_call_sequence = False

while ret:
    ret, img = cap.read()

    # Mirror image vertically
    img = cv2.flip(img, 0)

    # Converting the recorded image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Applying filter to remove impurities
    gray = cv2.bilateralFilter(gray, 5, 1, 1)

    # Detecting the face for the region of the image to be fed to the eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(300, 300))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # roi_face is the face which is input to the eye classifier
            roi_face = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))

            # Examining the length of the eyes object for eyes
            if len(eyes) >= 2:
                eye_open = True
                cv2.putText(img, "Eyes Open", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

                # If eyes were previously closed and blink was ongoing, end the blink
                if is_blinking:
                    is_blinking = False
                    blink_count += 1
                    
                    # If the time since the last blink is less than 50 milliseconds, it is a double blink
                    if time.time() - last_blink_time < blink_time_value:
                        print("Double blink detected")
                        last_blink_time = time.time()
                        
                        if start_call_sequence:
                            make_emergency_call()

                    else:
                        last_blink_time = time.time()

            else:
                eye_open = False
                cv2.putText(img, "Blink", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)

                # Start the blink if eyes were open in the previous frame
                if prev_eye_open:
                    is_blinking = True

            prev_eye_open = eye_open

    else:
        eye_open = False
        cv2.putText(img, "No face detected", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    # Controlling the algorithm with keys
    cv2.imshow("Mirrored Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('s'):
        print("calling enabled")
        start_call_sequence = True

cap.release()
cv2.destroyAllWindows()
