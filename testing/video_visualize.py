
import cv2
import imutils
import time



cap = cv2.VideoCapture('videos/1_3NeoLOCZONA_A-96H_C0A1_P1_N1.mp4')


ret, frame1 = cap.read()


while cap.isOpened():
    ret, new_frame = cap.read()
    if not ret:
        break

    cv2.imshow('Optical Flow', new_frame)
        # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()