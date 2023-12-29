# import the necessary packages
import argparse
import cv2
import numpy as np
import utils


#CONSTANTS
FRAME_TIME_DELTA = 0.333
# TODO: COLOCAR CONVERSÃO DE FRAME PARA CM

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=False,
	help="name video", default='1_3NeoLOCZONA_A-96H_C0A1_P1_N1.mp4')
args = vars(ap.parse_args())

path_video = 'videos/' + args['video']
print(path_video)

# Inicilização do vídeo
video = cv2.VideoCapture(path_video)
ret, frame1 = video.read()

# Delimitar o diâmetro do poço 
line = utils.get_pit_linepoints(frame1)
print(line)

# Define variáveis de interesse
centroid_positions = []
speed_vec = []
total_displacement = 0
inst_speed = 0
previous_position = None
debug = None


while video.isOpened():

    # Leitura do frame
    ret, frame = video.read()
    if not ret:
        break

    # Processo de detecção da planária
    centroid, debug, img_postproc = utils.detection(frame, line)


    # A partir daqui não implementado ainda.
    # Falta pegar o centróide direitinho.

    # Atualiza variáveis de interesse
    centroid_positions.append(centroid)
    current_position = centroid

    if previous_position is not None:
        # Calcular a distância entre as posições
        displacement = np.linalg.norm(np.array(current_position) - 
                                      np.array(previous_position))

        # Calcular a velocidade (supondo uma taxa de quadros fixa)
        # Você pode calcular o tempo entre os frames usando a taxa de quadros do vídeo
        inst_speed = displacement / FRAME_TIME_DELTA
        speed_vec.append(inst_speed)

        # Adicionar a distância percorrida ao deslocamento total
        total_displacement += displacement


    # print(current_position, inst_speed, total_displacement)

    # Apenas para debugar a trajetória
    debug = utils.draw_debug(img_postproc, debug, centroid_positions)
    cv2.imshow("Original", frame)
    cv2.imshow("Debug", debug)
    

        # Exit if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'): # Para não ficar parando
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Atualizar a posição anterior para o próximo cálculo
    previous_position = current_position


print("speed_vec: ", speed_vec)
print("total_displacement: ", total_displacement) # Sei q tem um jeito melhor de imprimir


video.release()

cv2.destroyAllWindows()





