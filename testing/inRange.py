# import cv2
# import numpy as np

# # Carregando a imagem
# imagem = cv2.imread('../videos/sample.png')

# # Convertendo a imagem para o espaço de cores HSV (Hue, Saturation, Value)
# imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
# imagem_gaus = cv2.GaussianBlur(imagem_hsv, (5, 5), 0)


# bgr_planaria = np.uint8([[[145, 158, 188]]])

# # Definindo os intervalos de cores para a planária vermelha (esses valores podem variar)
# # Aqui, definimos um intervalo para tons de vermelho
# hsv_planaria = cv2.cvtColor(bgr_planaria,cv2.COLOR_BGR2HSV)

# print(hsv_planaria)
# H = hsv_planaria[0,0,0]

# hsv_inferior = np.array([0, 10, 10])
# hsv_superior = np.array([H + 30, 255, 255])
# print(hsv_inferior, hsv_superior)
# # Criando uma máscara para segmentar a cor vermelha na imagem HSV
# mascara = cv2.inRange(imagem_hsv, hsv_inferior, hsv_superior)


# # Aplicando a máscara na imagem original para destacar a região correspondente à cor vermelha
# result = cv2.bitwise_and(imagem, imagem, mask=mascara)

# # Mostrando a imagem original e a região destacada correspondente à cor vermelha
# cv2.imshow('Imagem Original', imagem)
# cv2.imshow('Imagem HSV', imagem_hsv)
# cv2.imshow('Região Vermelha Detectada', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()








##########################################

import cv2 as cv
import argparse
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


# parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
# parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
# args = parser.parse_args()
# cap = cv.VideoCapture(args.camera)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
while True:
        
    # Carregando a imagem
    imagem = cv.imread('../videos/sample.png')
    imagem_gaus = cv.GaussianBlur(imagem, (3, 3), 0)
    # Convertendo a imagem para o espaço de cores HSV (Hue, Saturation, Value)
    imagem_hsv = cv.cvtColor(imagem_gaus, cv.COLOR_BGR2HSV)
    
    # ret, frame = cap.read()

    frame_threshold = cv.inRange(imagem_gaus, (low_H, low_S, low_V), (high_H, high_S, high_V))


    cv.imshow(window_capture_name, imagem)
    cv.imshow("gaus", imagem_gaus)
    cv.imshow("hsv", imagem_hsv)
    cv.imshow(window_detection_name, frame_threshold)

    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break
cv.destroyAllWindows()