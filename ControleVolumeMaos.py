# https://www.computervision.zone/lessons/gesture-control-video-lessons/
import cv2
import time
import numpy as np
import HandTrackingModule as htm

############################
# Parmâmetros de operação
wCam, hCam = 640, 480 # largura e altura da captura
tempo_anterior = 0
############################

# checar se camera funciona, em caso de erro colocar id = 1; 0 = open default camera
captura = cv2.VideoCapture(0) 

captura.set(3, wCam) # 3 = CAP_PROP_FRAME_WIDTH
captura.set(4, hCam) # 4 = CAP_PROP_FRAME_HEIGHT


detector = htm.handDetector()



# operação do programa
while True:
    success, img = captura.read() # teste de sucesso de captura
    
    # detectar a mão, enviando a imagem da camera para marcar os pontos da mão
    img = detector.findHands(img)
    # detectar a posição da mão
    lmList = detector.findPosition(img, draw=False)[0] # primeiro elemento tem os pontos da mão
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        
        # capturando as cordenadas x, y da ponta do polegar[4] e do indicador[8]
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
    # ajuste dop FrameRate
    tempo_captura = time.time()
    fps = 1/(tempo_captura - tempo_anterior)
    tempo_anterior = tempo_captura
    
    # apresenta FPS npo canto superior esquerdo
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow('Img', img) 
    cv2.waitKey(1) # 1ms de delay
    
    