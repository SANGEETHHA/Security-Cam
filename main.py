import cv2
import pygame
pygame.mixer.init()

# Check available camera indices
for index in range(9):  # Try indices from 0 to 9
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera index {index} is not available.")
    else:
        print(f"Camera index {index} is available.")
        cap.release()

# Specify a valid camera index
cam = cv2.VideoCapture(0)  # Use a valid camera index (e.g., 0) based on your system

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 1000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        alert_sound = pygame.mixer.Sound('alert.wav')
        alert_sound.play()

    if cv2.waitKey(10) == ord('q'):
        break

    cv2.imshow('Granny Cam', frame1)

# Release the camera and close OpenCV windows
cam.release()
cv2.destroyAllWindows()
