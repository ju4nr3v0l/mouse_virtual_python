#---------------- IMportamos la librerias -----------------------------
import cv2
import numpy as np
import SeguimientoManos as sm
import autopy # libreria para manipular el mouse

#------------------------- declaracion de variables ---------#
anchocam, altocam, = 640, 480
cuadro = 100
anchopanta, altopanta = autopy.screen.size()
sua = 8
pubix, pubiy = 0,0
cubix, cubiy = 0,0


#---------------------------- lectura de la camara -----------------------------------#
cap = cv2.VideoCapture(0)
cap.set(3,anchocam)
cap.set(4,altocam)

#------ declarar el detector ----------#
detector = sm.detectormanos(maxManos=1) # para mouse solo vamos a usar 1 mano
while True:
    #-------- econtar los puntos de las manos ---------#
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame) #encontramos la mano
    lista, bbox = detector.encontrarposicion(frame) # encontramos la posicion de la mano

    #---------------- obtener la punta del dedo indice y medio --------#
    if (len(lista)) != 0:
        x1, y1 = lista[8][1:] # coordenadas de dedo indice
        x2, y2 = lista[12][1:] # coordenadas de dedo medio



        #-------- comprobar que dedos esten arriba ------#
        dedos = detector.dedosarriba()

        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0,0,0),2) #generando cuadro de deteccion
        #--------- modo movimiento solo dedo indice ---------#
        if dedos[1] == 1 and dedos[2] == 0: # si indice arriba pero medio abajo

            #------------- convertir movimiento a pixeles -------#
            x3 = np.interp(x1, (cuadro, anchocam-cuadro),(0,anchopanta))
            y3 = np.interp(y1, (cuadro, altocam-cuadro),(0,altopanta))

            #---------------------suavizado ------------------------#
            cubix = pubix + (x3 - pubix) / sua
            cubiy = pubiy + (y3 - pubiy) / sua

            # mover el mouse
            autopy.mouse.move(anchopanta - cubix,cubiy)
            cv2.circle(frame, (x1,y1), 10, (0,0,0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        #------------- comprobar si hacemos click ---------------------#
        if dedos[1] == 1 and dedos[2] == 1:
            #--------------- comprobar distancia entre dedos ---------------------------------#
            longitud, frame, linea = detector.distancia(8,12,frame)
            print(longitud)
            if longitud < 30:
                cv2.circle(frame, (linea[4],linea[5]),10,(0,255,0), cv2.FILLED)

                #hacer click
                autopy.mouse.click()


    cv2.imshow("Mouse",frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

