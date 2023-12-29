# import the necessary packages
import argparse
import cv2
import numpy as np

cap = cv2.VideoCapture('videos/1_3NeoLOCZONA_A-96H_C0A1_P1_N1.mp4')

ret, frame1 = cap.read()


while cap.isOpened():
    ret, new_frame = cap.read()
    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    if not ret:
        break
    
    cv2.imshow("Original", new_frame)
    bloco = 25 # bloco define o tamanho da vizinhança usada para calcular o threshold adaptativo
    C = 13 # constante subtraída da média ou ponderação na média.

    thresh = cv2.adaptiveThreshold(blurred, 255,
	                            cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY_INV, bloco, C)
    
    
    eroded = cv2.erode(thresh.copy(), None, iterations=1)
    dilated = cv2.dilate(eroded.copy(), None, iterations=1)
    #closing para evitar partes quebradas
    kernelSize = (3, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    img_post_proc = closing
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
	# can be MORPH_ELLIPSE or MORPH_CROSS or another
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
     
    # find contours in the binary image
    contours, hierarchy = cv2.findContours(img_post_proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rgb_img = cv2.cvtColor(img_post_proc, cv2.COLOR_GRAY2BGR)
    # https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
    print(len(contours))
    cv2.drawContours(rgb_img, contours, -1, (0, 255, 0), 1)
    for c in contours:
        # print(c)
        # calculate moments for each contour
        M = cv2.moments(c)
        area = M["m00"]
        print('area:', area)
        if area < 800:
            # calculate x,y coordinate of center
            cX = int(M["m10"] / (M["m00"] + 1e-4))
            cY = int(M["m01"] / (M["m00"] + 1e-4))
            cv2.circle(rgb_img, (cX, cY), 1, (0, 0, 255), 1)
            cv2.putText(rgb_img, str(M["m00"]), (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            # cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    # thresh_inv = cv2.bitwise_not(rgb_img)
# # Detectando círculos (para tentar definir o poço)
#     rows = gray.shape[0]
#     # circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT_ALT, 5, rows / 4,
#     #                            param1=300, param2=.8,
#     #                            minRadius=0, maxRadius=0)
#     circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, rows / 4,
#                                param1=30, param2=30,
#                                minRadius=0, maxRadius=0)
#     # print(circles)
#     
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for i in circles[0, :]:
#             center = (i[0], i[1])
#             # circle center
#             cv2.circle(rgb_img, center, 2, (0, 0, 255), 2)
#             cv2.circle(new_frame, center, 2, (0, 0, 255), 2)
#             # circle outline
#             radius = i[2]
#             cv2.circle(rgb_img, center, radius, (255, 0, 0), 2)
#             cv2.circle(new_frame, center, radius, (255, 0, 0), 2)

#             print(radius)
    
    # cv2.imshow("Opening", opening)
    cv2.imshow("dilated", dilated)
    cv2.imshow("RGB", rgb_img)
    cv2.imshow("Original", new_frame)
        # Exit if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break



cap.release()

cv2.destroyAllWindows()