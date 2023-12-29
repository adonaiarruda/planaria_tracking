import cv2

# Função 'A' que executa a lógica do desenho da linha e retorna os pontos finais
def get_linepoints(img):
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

# Carregar a imagem
imagem = cv2.imread('../videos/sample.png')

# Exemplo de uso da função 'A'
ponto_inicial, ponto_final = get_linepoints(imagem)
print("Ponto inicial:", ponto_inicial)
print("Ponto final:", ponto_final)

