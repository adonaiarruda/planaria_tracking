import cv2
import math
import numpy as np

## Constants
# Preprocessing
BLUR_KERNEL = (7,7)
# Thresholding
BLOCO = 25 # bloco define o tamanho da vizinhança usada para calcular o threshold adaptativo
C = 13 # constante subtraída da média ou ponderação na média.
# Postprocessing
CLOSING_KERNEL = (3, 3)
# Centroid finding
MAX_AREA = 800
MIN_AREA = 20


def preprocessing(img):

    # Converte imagem em cinza e aplica filtro gaussiano
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
    return blurred

def postprocessing(img):
    eroded = cv2.erode(img, None, iterations=1)
    dilated = cv2.dilate(eroded, None, iterations=1)
    #closing para evitar partes quebradas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, CLOSING_KERNEL)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    return closing

def distancia_entre_pontos(ponto1, ponto2):
    return math.sqrt((ponto2[0] - ponto1[0])**2 + (ponto2[1] - ponto1[1])**2)


def find_centroid(img, line):

    debug = {}
    debug['contours'] = []
    debug['areas'] = []
    debug['centers'] = []
    debug['planarian'] = None
    debug['pit'] = (0,0)
    
    # find contours in the binary image
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
    # print(len(contours))
    # cv2.drawContours(rgb_img, contours, -1, (0, 255, 0), 1)

    detected_centroids = []
    planarian_centroid = (0,0)
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)
        area = M["m00"]
        # print('area:', area)
        if MIN_AREA < area < MAX_AREA:
            # calculate x,y coordinate of center
            cX = int(M["m10"] / (M["m00"] + 1e-4))
            cY = int(M["m01"] / (M["m00"] + 1e-4))

            detected_centroids.append((cX, cY))

            # cv2.circle(rgb_img, (cX, cY), 1, (0, 0, 255), 1)
            # cv2.putText(rgb_img, str(area), 
            #             (cX - TEXT_POS, cY - TEXT_POS), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.5, (0, 0, 255), 1)
            debug['contours'].append(c)
            debug['centers'].append((cX, cY))
            debug['areas'].append(area)
            
    # TODO:
            # Encontrar maior centroide que está próximo ao centro do poço. Retornar (cx,cy) único
            # Usar variável line
            # Desenhar o circulo estimado do poço em rgb_img
        if len(detected_centroids) > 0:
            pit_center = (int((line[0][0]+line[1][0])/2), 
                        int((line[0][1]+line[1][1])/2))
            # print(line_center)
            pit_radio = int(np.linalg.norm(np.array(line[0]) - 
                                       np.array(pit_center)))
            planarian_centroid = min(detected_centroids, 
                                    key=lambda ponto: distancia_entre_pontos(pit_center, ponto))
            
            # cv2.circle(rgb_img, planarian_centroid, 1, (0, 0, 255), 1)
            # cv2.circle(rgb_img, pit_center, pit_radio, (255, 0, 0), 1)
            debug['planarian'] = planarian_centroid
            debug['pit'] = (pit_center, pit_radio)



    return planarian_centroid, debug


def detection(frame, line):

    img_preproc = preprocessing(frame)

    thresh = cv2.adaptiveThreshold(img_preproc, 255,
	                            cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY_INV, BLOCO, C)

    img_postproc = postprocessing(thresh)

    centroid, debug = find_centroid(img_postproc, line)

    return centroid, debug, img_postproc

def draw_debug(img, debug, centroid_positions):
    rgb_img = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)
    TEXT_POS = -10
    # print(debug)
    cv2.drawContours(rgb_img, debug['contours'], -1, (0, 255, 0), 1)

    for i in range(len(debug['areas'])):
        cv2.putText(rgb_img, str(debug['areas'][i]), 
                    (debug['centers'][i][0] - TEXT_POS, 
                     debug['centers'][i][1] - TEXT_POS), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 0, 255), 1)
        
    
    cv2.circle(rgb_img, debug['planarian'], 1, (0, 0, 255), 1)
    cv2.circle(rgb_img, 
               debug['pit'][0], 
               debug['pit'][1], 
               (255, 0, 0), 1)
    
    for i in range(len(centroid_positions)-1):
        cv2.line(rgb_img, centroid_positions[i+1], 
                 centroid_positions[i], (0, 155, 155), 
                 1) 

    return rgb_img



def get_pit_linepoints(img):
    ponto1 = (-1, -1)
    ponto2 = (-1, -1)

    # Função de callback do mouse
    def draw_line(event, x, y, flags, param):
        nonlocal ponto1, ponto2

        if event == cv2.EVENT_LBUTTONDOWN:
            ponto1 = (x, y)
            param['drawing'] = True
            # Limpar a imagem para desenhar uma nova linha
            param['imagem'] = param['imagem_original'].copy()
        elif event == cv2.EVENT_MOUSEMOVE:
            if param['drawing']:
                ponto2 = (x, y)
                img_copy = param['imagem'].copy()
                cv2.line(img_copy, ponto1, ponto2, (255, 0, 0), 1)
                cv2.imshow('Desenhar Linha', img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            param['drawing'] = False
            ponto2 = (x, y)
            cv2.line(param['imagem'], ponto1, ponto2, (255, 0, 0), 2)
            cv2.imshow('Desenhar Linha', param['imagem'])

    # Carregar a imagem
    cv2.imshow('Desenhar Linha', img)

    # Dicionário para armazenar informações dos pontos e do estado do desenho
    info_desenho = {'drawing': False, 'imagem': img.copy(), 'imagem_original': img}

    cv2.setMouseCallback('Desenhar Linha', draw_line, info_desenho)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Pressione 'Esc' para sair
            break

    cv2.destroyAllWindows()
    return ponto1, ponto2
