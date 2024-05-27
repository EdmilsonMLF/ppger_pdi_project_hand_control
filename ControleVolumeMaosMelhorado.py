# https://www.computervision.zone/lessons/gesture-control-video-lessons/
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
# controle de audio com https://github.com/AndreMiras/pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 

# parametros da biblioteca de audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Parmâmetros de operação da camera
wCam = 640 # largura da captura
hCam = 480 # altura da captura
tempo_anterior = 0

# parametros iniciais de volume
ajuste_volume = 0
ajuste_volume_tela = 400
ajuste_volume_percentual = 0
area = 0
cor_volume = (0, 255, 0)
#capturando volume mínimo e máximo do sistema
VOLUME_RANGE = volume.GetVolumeRange()
VOLUME_MIN = VOLUME_RANGE[0]
VOLUME_MAX = VOLUME_RANGE[1]

# checar se camera funciona, em caso de erro colocar id = 1; 0 = open default camera
captura = cv2.VideoCapture(0) 
captura.set(3, wCam) # 3 = CAP_PROP_FRAME_WIDTH
captura.set(4, hCam) # 4 = CAP_PROP_FRAME_HEIGHT
detector = htm.handDetector(maxHands=1)

# operação do programa
while True:
    success, img = captura.read() # teste de sucesso de captura
    
    # Detectar a mão, enviando a imagem da camera para marcar os pontos da mão
    img = detector.findHands(img)
    # detectar a posição da mão
    lmList, bbox = detector.findPosition(img, draw=True) # primeiro elemento tem os pontos da mão

    if len(lmList) != 0:
        
        # Filtrar baseado no tamanho da mão
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        if 300 < area < 900:
            # Encontrar a distancia entre polegar (4) e indicador (8)
            tamanho_linha, img, coord_linha = detector.findDistance(4, 8, img)
            # Converter Volume
                # converter o range da distancia entre os dedos e o range do volume do pc
                # Range da mão 40 - 250
                # Range do volume -63 - 0
            
            # novo range para controle do volume
            ajuste_volume_tela = np.interp(
                tamanho_linha, 
                [40, 250], 
                [400, 150]
            ) 
            # novo range para apresentação em tela
            ajuste_volume_percentual = np.interp(
                tamanho_linha, 
                [40, 250], 
                [0, 100]
            ) 
            
            # Reduzir resolução para suavizar
            suavizador = 10
            ajuste_volume_percentual = suavizador * (ajuste_volume_percentual / suavizador)
            # Verificar se os dedos estão para cima
            dedos = detector.fingersUp()
            print(dedos)
            
            # Se mindinho estiver para baixo, defina o volume
            if not dedos[4]:
                # ajustar o volume do sistema com os dedos
                volume.SetMasterVolumeLevelScalar(ajuste_volume_percentual/100, None)
                # criando efeito botão 
                cv2.circle(
                    img, 
                    (coord_linha[4], coord_linha[5]), 
                    10, 
                    (0, 255, 0), 
                    cv2.FILLED
                )
                cor_volume = (0, 255, 0)
            else:
                cor_volume = (255, 0, 0)
            
    # Desenhar na imagem         
              
    # colocar o volume do sistema na imagem
    cv2.rectangle(
        img, 
        (50, 150), 
        (85, 400), 
        (0, 255, 0), 
        3 
    ) 
    cv2.rectangle(
        img, 
        (50, int(ajuste_volume_tela)), 
        (85, 400), 
        (255, 0, 0), 
        cv2.FILLED 
    )  
    
    # apresenta % do volume na tela
    cv2.putText(
        img, 
        f'Volume: {int(ajuste_volume_percentual)} %', 
        (40, 450),
        cv2.FONT_HERSHEY_PLAIN, 
        2, 
        (255, 0, 0), 
        3
    )
    volume_atual = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(
        img, 
        f'Volume Def.: {int(volume_atual)} %', 
        (300, 50),
        cv2.FONT_HERSHEY_PLAIN, 
        2, 
        cor_volume, 
        3
    )
    
    # Imprimir FPS    
    # ajuste dop FrameRate
    tempo_captura = time.time()
    fps = 1/(tempo_captura - tempo_anterior)
    tempo_anterior = tempo_captura
    
    # apresenta FPS npo canto superior esquerdo
    cv2.putText(
        img, 
        f'FPS: {int(fps)}', 
        (40, 50),
        cv2.FONT_HERSHEY_PLAIN, 
        2, 
        (255, 0, 0), 
        3
        )
    cv2.imshow('Img', img) 
    cv2.waitKey(1) # 1ms de delay
    
    