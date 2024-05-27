# https://www.computervision.zone/lessons/gesture-control-video-lessons/
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # controle de audio com https://github.com/AndreMiras/pycaw

# parametros da biblioteca de audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Parmâmetros de operação da camera
wCam, hCam = 640, 480 # largura e altura da captura
tempo_anterior = 0

# parametros iniciais de volume
ajuste_volume = 0
ajuste_volume_tela = 400
ajuste_volume_percentual = 0

#capturando volume mínimo e máximo do sistema
VOLUME_RANGE = volume.GetVolumeRange()
VOLUME_MIN = VOLUME_RANGE[0]
VOLUME_MAX = VOLUME_RANGE[1]

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
    lmList, bbox = detector.findPosition(img, draw=True) # primeiro elemento tem os pontos da mão

    if len(lmList) != 0:
        
        # Filtrar baseado no tamanho da mão
        print(bbox)
        # Encontrar a distancia entre polegar e indicador
        
        # Converter Volume
        
        # Reduzir resolução para suavizar
        
        # Verificar se os dedos estão para cima
        
        # verificar se mindinho esta para baixo para definir o volume
        
        # desenhar na imagem
        
        # Imprimir FPS
        
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
        
        # criando efeito botão 
        if tamanho_linha < 40:
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        
        # converter o range da distancia entre os dedos e o range do volume do pc
        # Range da mão 40 - 250
        # Range do volume -63 - 0
        ajuste_volume = np.interp(tamanho_linha, [40, 250], [VOLUME_MIN, VOLUME_MAX])  # novo range para controle do volume
        ajuste_volume_tela = np.interp(tamanho_linha, [40, 250], [400, 150]) # novo range para apresentação em tela
        ajuste_volume_percentual = np.interp(tamanho_linha, [40, 250], [0, 100]) # novo range para apresentação em tela
        
        # ajustar o volume do sistema com os dedos
        volume.SetMasterVolumeLevel(ajuste_volume, None)
              
    # colocar o volume do sistema na imagem
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3 ) 
    cv2.rectangle(img, (50, int(ajuste_volume_tela)), (85, 400), (255, 0, 0), cv2.FILLED )  
    
    # apresenta % do volume na tela
    cv2.putText(img, f'Volume: {int(ajuste_volume_percentual)} %', (40, 450),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        
    # ajuste dop FrameRate
    tempo_captura = time.time()
    fps = 1/(tempo_captura - tempo_anterior)
    tempo_anterior = tempo_captura
    
    # apresenta FPS npo canto superior esquerdo
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow('Img', img) 
    cv2.waitKey(1) # 1ms de delay
    
    