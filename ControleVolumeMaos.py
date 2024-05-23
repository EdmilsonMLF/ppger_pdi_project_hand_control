# https://www.computervision.zone/lessons/gesture-control-video-lessons/
import cv2
import time
import numpy as np

############################
# Parmâmetros de operação
wCam, hCam = 640, 480 # largura e altura da captura
tempo_anterior = 0
############################

# checar se camera funciona, em caso de erro colocar id = 1; 0 = open default camera
captura = cv2.VideoCapture(0) 

captura.set(3, wCam) # 3 = CAP_PROP_FRAME_WIDTH
captura.set(4, hCam) # 4 = CAP_PROP_FRAME_HEIGHT

# operação do programa
while True:
    success, img = captura.read() # teste de sucesso de captura
    
    # ajuste dop FrameRate
    tempo_captura = time.time()
    fps = 1/(tempo_captura - tempo_anterior)
    tempo_anterior = tempo_captura
    
    # apresenta FPS npo canto superior esquerdo
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow('Img', img) 
    cv2.waitKey(1) # 1ms de delay
    
    