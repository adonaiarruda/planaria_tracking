# import the necessary packages
import argparse
import cv2
import numpy as np
from scipy import ndimage 


cap = cv2.VideoCapture('../videos/1_3NeoLOCZONA_A-96H_C0A1_P1_N1.mp4')


ret, frame1 = cap.read()

# Possibilidade de achar os circulos

while cap.isOpened():
    ret, new_frame = cap.read()
    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    if not ret:
        break
    

          
    roberts_cross_v = np.array( [[1, 0 ], 
                                [0,-1 ]] ) 
    
    roberts_cross_h = np.array( [[ 0, 1 ], 
                                [ -1, 0 ]] ) 
    
    img = gray.astype('float64') 
    img /= 255.0
    vertical = ndimage.convolve( img, roberts_cross_v ) 
    horizontal = ndimage.convolve( img, roberts_cross_h ) 
    
    edged_img = np.sqrt( np.square(horizontal) + np.square(vertical)) 
    edged_img*=255
    cv2.imshow("test", gray)




    # cv2.imshow("Original", new_frame)
    # thresh = cv2.adaptiveThreshold(blurred, 255,
	# cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    # eroded = cv2.erode(thresh.copy(), None, iterations=1)
    # dilated = cv2.dilate(eroded.copy(), None, iterations=1)

   
    cv2.imshow("Original", new_frame)
        # Exit if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break



cap.release()

import cv2  
import numpy as np 

  
roberts_cross_v = np.array( [[1, 0 ], 
                             [0,-1 ]] ) 
  
roberts_cross_h = np.array( [[ 0, 1 ], 
                             [ -1, 0 ]] ) 
  
img = cv2.imread("input.webp",0).astype('float64') 
img/=255.0
vertical = ndimage.convolve( img, roberts_cross_v ) 
horizontal = ndimage.convolve( img, roberts_cross_h ) 
  
edged_img = np.sqrt( np.square(horizontal) + np.square(vertical)) 
edged_img*=255
cv2.imwrite("output.jpg",edged_img)
