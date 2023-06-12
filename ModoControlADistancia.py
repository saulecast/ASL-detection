# Esta es una copia para beige del codigo que escribí llamado Mouse_mano
# la inspiración y el modulo HandTrackingModule es de un canal de youtube 
# llamado MurtazasWorkshopRoboticsandAI pero yo le hice bastantes cambios, mejoras y adaptación

import cv2 as cv
import numpy as np
import time
import autopy
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
wScr, hScr = autopy.screen.size() #las dimensiones de la pantalla
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

        #4. Ver que solo el dedo indice esté arriba (mueve el mouse)
        if dedos[1]==1 and dedos[2]==0: #dedos[1] es el indice dedos[2] es el dedo mayor, se puede entender viendo el HandTrackingModule.py en al fucnión fingersUp()
            #5. Convertir Coordenadas desde el rectangulo que creamos para el tamaño real de la pantalla
            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr)) #(0, wCam) hubiera tomado la pantalla completa, simplemente delimitamos a dentro del rectangulo
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            
            #6. Limpiar los valores para que el mouse no tiemble
            clocx = plocx + (x3 - plocx) / smoothening
            clocy = plocy + (y3 - plocy) / smoothening

            #7. Mover Mouse hacia las coordenadas leidas de nuestra mano con un dedo levantado y luego covertidas para adaptarse al tamaño real de la pantalla
            autopy.mouse.move(clocx, clocy)
            cv.circle(img, (x1,y1), 15, (255,0,255), cv.FILLED)
            plocx, plocy = clocx, clocy

        #8. Ver si tanto el indice como el mayor está levantados (hace click)
        if dedos[1] == 1 and dedos[2] == 1:

            #9. encontrar distancia entre dedos indice y mayor
            distancia, img, line_info = detector.findDistance(8, 12, img) #8 y 12 son los puntos de referencia ubicados en la mano que hacen referencia a el la punto del dedo indice y mayor respectivamente
            print(distancia)

            #10. Hacer click
            if distancia < 30: #acerca los dos dedos para hacer click
                cv.circle(img, (line_info[4], line_info[5]), #los line_info son coordenadas identificables del HandTrackingModule.py
                        15, (0, 255, 0), cv.FILLED)
                autopy.mouse.click()

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

