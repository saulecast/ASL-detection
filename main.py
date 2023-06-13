# Esta es una copia para beige del codigo que escribí llamado Mouse_mano
# la inspiración y el modulo HandTrackingModule es de un canal de youtube 
# llamado MurtazasWorkshopRoboticsandAI pero yo le hice bastantes cambios, mejoras y adaptación

import cv2 as cv
import numpy as np
import time
import HandTrackingModule as htm

#########################
wCam, hCam = 648, 480 #definimos las dimensiones de la ventana de la camara
frameR= 100 #reducción de tamaño de la pantalla de la camara (frame reduction)
smoothening = 3 #es para limpiar un poco las coordenadas del mouse y mejorar su fluidez, si deseas aumentar su sensibilidad solo reduce este número y biseversa
#########################

antes = 0
plocx, plocy = 0, 0 #previous location (lugar anterior) en x e y
clocx, clocy = 0, 0 #current location (lugar actual) en x y y

cam = cv.VideoCapture(0)
cam.set(3, wCam) #ancho de cam
cam.set(4, hCam)  #largo de cam
# print (f'Las dimensiones son ancho={wScr}, alto ={hScr}')

detector = htm.handDetector(maxHands=1)
while True:
    next, img = cam.read() #img es más corto que 'fotograma' así que he decidido nombrarlo así
    img = cv.flip(img, 1) #para evitar el efecto espejo

    #Encontrar puntos de referencia en las manos
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #Encontrar las puntos de los dedos indice y mayor
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(f'posición de indice=({x1},{y1}) , posición de mayor=({x2},{y2})')

        #Ver cual dedo está levantado
        dedos = detector.fingersUp()
        # print(dedos) #mediante una lista, nos permite ver qué dedos están levantados
        
        #determinar el area dentro de la cual se detecta mi movimiento... para poner un borde inferior comodo y que no se haga incomodo cuando esté bajando la mano
        cv.rectangle(img, (frameR,frameR), (wCam-frameR, hCam-frameR), 
                (255,0,255), 2)



    #frame rate
    ahora = time.time()
    try:
        fps = 1 / (ahora - antes)
    except: 
        pass
    antes = ahora
    cv.putText(img, f'fps={str(int(fps))}', (20,50), cv.FONT_HERSHEY_SIMPLEX, 0.7,
            (255,0,0), 2)
    #display
    cv.imshow("camara", img)
    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

