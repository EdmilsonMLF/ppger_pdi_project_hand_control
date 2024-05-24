# https://www.computervision.zone/lessons/gesture-control-video-lessons/
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
# controle de audio com https://github.com/AndreMiras/pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# parametros da biblioteca de audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Parmâmetros de operação da camera
wCam, hCam = 640, 480 # largura e altura da captura
tempo_anterior = 0

#capturando volume mínimo e máximo do sistema
VOLUME_RANGE = volume.GetVolumeRange()
VOLUME_MIN = VOLUME_RANGE[0]
VOLUME_MAX = VOLUME_RANGE[1]
# volume.SetMasterVolumeLevel(-20.0, None)

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
        # manual: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
        
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # ponto médio da distancia entre a ponta dos dedos polegar e indicador
        
        
        #criando circulos na ponta dos dedos
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        
        # linha entre as pontas dos dedos
        cv2.line(img, (x1, y1), (x2,y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        
        tamanho_linha = math.hypot(x2 - x1, y2 - y1) # tamanho da linha varia com a distância da mão para a câmera além da distancia entre os dedos
        print(tamanho_linha)
        
        # criando efeito botão 
        if tamanho_linha < 40:
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        
        
        
    # ajuste dop FrameRate
    tempo_captura = time.time()
    fps = 1/(tempo_captura - tempo_anterior)
    tempo_anterior = tempo_captura
    
    # apresenta FPS npo canto superior esquerdo
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow('Img', img) 
    cv2.waitKey(1) # 1ms de delay
    
    