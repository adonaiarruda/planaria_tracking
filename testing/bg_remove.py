import cv2

image_path = "./videos/sample.png"
image = cv2.imread(image_path)

#resizing the image
desired_width = 400  
aspect_ratio = image.shape[1] / image.shape[0]
desired_height = int(desired_width / aspect_ratio)
resized_image = cv2.resize(image, (desired_width, desired_height))

def onTrackbarChange(value):
    global blk_thresh
    blk_thresh = value
    print("Variable value:", blk_thresh)
    
def valueScaling(value):
    min_value = 0
    max_value = 100
    new_min = 0
    new_max = 255
    scaled_value = (value - min_value) * (new_max - new_min) / (max_value - min_value) + new_min
    return int(scaled_value)


blk_thresh = 50
scaled_thresh = valueScaling(blk_thresh)


window_name = 'Background Removed'
cv2.namedWindow(window_name)

cv2.createTrackbar('Variable', window_name, scaled_thresh, 100, onTrackbarChange)

while True:
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold_img = cv2.threshold(blur, blk_thresh, 255, cv2.THRESH_BINARY)

    mask = 255 - threshold_img

    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    cv2.imshow(window_name, result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
