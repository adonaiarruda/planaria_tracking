# import the necessary packages
import argparse
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to input image", default='car.png')
args = vars(ap.parse_args())

# load the image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# construct a rectangular kernel (13x5) and apply a blackhat
# operation which enables us to find dark regions on a light
# background
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

# similarly, a tophat (also called a "whitehat") operation will
# enable us to find light regions on a dark background
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
# show the output images
cv2.imshow("Gray", gray)
cv2.imshow("Original", image)
cv2.imshow("Blackhat", blackhat)
cv2.imshow("Tophat", tophat)


# thresh = cv2.threshold(tophat,210,255,cv2.THRESH_BINARY)
# cv2.imshow("Thresholding", thresh)

cv2.waitKey(0)