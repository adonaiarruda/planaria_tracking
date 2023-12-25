# Versão inicial, para testar filtragens e detecções iniciais

# Tarefa 1 -> identificar circulo do poço
# Referência: https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
import cv2
import sys
import numpy as np

# Tentar identificar edges primeiro e depois identificar o circulo




def main(argv):
    
    default_file = 'videos/sample.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv2.imread(cv2.samples.findFile(filename), cv2.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    
    gray = cv2.medianBlur(gray, 5)

    cv2.imshow("gray", gray)
    
    rows = gray.shape[0]
    
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 4,
                               param1=30, param2=30,
                               minRadius=0, maxRadius=0)
    # todo: testar parametros para identificar o circulo do poço
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(src, center, 1, (0, 100, 100), 1)
            # circle outline
            radius = i[2]
            cv2.circle(src, center, radius, (255, 0, 255), 1)
    
    
    cv2.imshow("detected circles", src)
    cv2.waitKey(0)
    
    return 0
if __name__ == "__main__":
    main(sys.argv[1:])