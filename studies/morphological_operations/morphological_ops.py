# import the necessary packages
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to input image", default='pyimagesearch_logo.png')
# ap.add_argument("-i", "--image", required=False,
# 	help="path to input image", default='pyimagesearch_logo_noise.png')
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and display it to our
# screen
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Original", image)

## Erosion -> Reduce small blobs connecting objects
    # Useful to remove joining parts
# apply a series of erosions
for i in range(0, 3):
	eroded = cv2.erode(gray.copy(), None, iterations=i + 1)
	cv2.imshow("Eroded {} times".format(i + 1), eroded)
	cv2.waitKey(0)

## Dilation -> Opposite of erosion
	# Useful to joining broken parts
# close all windows to cleanup the screen 
cv2.destroyAllWindows()
cv2.imshow("Original", image)
# apply a series of dilations
for i in range(0, 3):
	dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)
	cv2.imshow("Dilated {} times".format(i + 1), dilated)
	cv2.waitKey(0)

## Opening -> remove small blobs
# close all windows to cleanup the screen, then initialize a list of
# of kernels sizes that will be applied to the image
cv2.destroyAllWindows()
cv2.imshow("Original", image)
kernelSizes = [(3, 3), (5, 5), (7, 7)]
# loop over the kernels sizes
for kernelSize in kernelSizes:
	# construct a rectangular kernel from the current size and then
	# apply an "opening" operation
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
	# can be MORPH_ELLIPSE or MORPH_CROSS or another
	opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
	# it allows us to pass in whichever morphological operation we want, followed by our kernel/structuring element.
	#Opening involves erosion followed by dilation in the outer surface (the foreground) of the image. 
	    # All the above-said constraints for erosion and dilation applies here. 
	    # It is a blend of the two prime methods. 
	    #It is generally used to remove the noise in the image.
	cv2.imshow("Opening: ({}, {})".format(
		kernelSize[0], kernelSize[1]), opening)
	cv2.waitKey(0)

# Closing
	# closing is used to close holes inside of objects or for connecting components together.
# close all windows to cleanup the screen
cv2.destroyAllWindows()
cv2.imshow("Original", image)
# loop over the kernels sizes again
for kernelSize in kernelSizes:
	# construct a rectangular kernel form the current size, but this
	# time apply a "closing" operation
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
	closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
	cv2.imshow("Closing: ({}, {})".format(
		kernelSize[0], kernelSize[1]), closing)
	cv2.waitKey(0)
	
# Morphological gradient
	# difference between a dilation and erosion. It is useful for determining the outline of a particular object of an image:

# close all windows to cleanup the screen
cv2.destroyAllWindows()
cv2.imshow("Original", image)
# loop over the kernels a final time
for kernelSize in kernelSizes:
	# construct a rectangular kernel and apply a "morphological
	# gradient" operation to the image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
	gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
	cv2.imshow("Gradient: ({}, {})".format(
		kernelSize[0], kernelSize[1]), gradient)
	cv2.waitKey(0)
	
