#!/usr/bin/env python

"""

Filename: clientepfc.py

Description: Contiene la clase principal Cliente_pfc y KeyboardControlThread.
La clase Cliente_pfc pone en funcionamiento la GUI y lleva a cabo el procesamiento 
del control del iRobot Create mediante reconociemiento visual utilizando los 
algoritmos de vision artificial de OpenCV. Es tambien la encargada de enviar la 
informacion a la maquina servidor, que controla el robot.
La clase KeyboardControlThread es el hilo que se encarga del control del robot
mediante los botones de la interfaz grafica.

"""

import sys
import signal # Modulo que proporciona mecanismos de gestion de eventos asincronos del sistema.

# Cargamos los modulos de Qt necesarios para el programa.
from PyQt4 import uic, QtGui, QtCore

# Cargamos el modulo de OpenCV.
import cv2
import numpy as np #Libreria de computacion cientifica. Utilizada para el procesamiento de arrays.

# Cargamos otras librerias
import Queue
import threading 
import time
import socket
from time import sleep
from threading import Thread

# Constantes 
ID_STOP = "01"
ID_UP = "02"
ID_UPP = "002"
ID_UPPP = "0002"
ID_DOWN = "03"
ID_DOWNN = "003"
ID_DOWNNN = "0003"
ID_LEFT = "04"
ID_RIGHT = "05"

# Variables globales
q = Queue.Queue()
move = "0"
prioridadBotones = False 
connection = False

#Preguntamos por los argumentos de entrada para arrancar la aplicacion
arglen=len(sys.argv)
if arglen<2:
    print('please run as python clientepfc.py <ip_address>')
    exit()

#Creamos el socket, establecemos el puerto correspondiente y lanzamos la conexion
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9999
clientSocket.connect((sys.argv[1], port))

#--------------------------------------------------------------
# Clase Cliente_pfc
#--------------------------------------------------------------
class Cliente_pfc:

    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi('gui.ui')

        # Tomamos el dispositivo de captura a partir de la webcam.
        self.webcam = cv2.VideoCapture(0)

        # Creamos un temporizador. Una vez cumplido el tiempo limite, se toma una captura desde la webcam.
        self.timer = QtCore.QTimer(self.MainWindow);

        # Conectamos la senal timeout() que emite nuestro temporizador con la funcion activity_frame().
        self.MainWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), self.activity_frame)

        # Tomamos una captura cada 1 milisegundo.
        self.timer.start(1);

        # Definimos los botones de la GUI
        self.connectKc = self.MainWindow.connectButton
        self.disconnectKc = self.MainWindow.disconnectButton
        self.exitKc = self.MainWindow.exitButton

        self.stopKC = self.MainWindow.stopButtonKC
        self.upKC = self.MainWindow.upButton
        self.downKC = self.MainWindow.downButton
        self.leftKC = self.MainWindow.leftButton
        self.rightKC = self.MainWindow.rightButton

        self.disconnectKc.setEnabled(False)
        self.stopKC.setEnabled(False)
        self.upKC.setEnabled(False)
        self.downKC.setEnabled(False)
        self.leftKC.setEnabled(False)
        self.rightKC.setEnabled(False)

        # Connect: realizamos la conexion de los signals y los slots
        self.connectKc.clicked.connect(self.establishConnection)
        self.disconnectKc.clicked.connect(self.disconnection)
        self. exitKc.clicked.connect(self.exitApplication)

        self.stopKC.clicked.connect(self.pushStopKC)
        self.upKC.clicked.connect(self.pushUpKC)
        self.downKC.clicked.connect(self.pushDownKC)
        self.leftKC.clicked.connect(self.pushLeftKC)
        self.rightKC.clicked.connect(self.pushRightKC)

    def activity_frame(self):
        """

        Es la funcion principal del reconocimiento visual.
        Toma la captura desde la webcam, la incorpora al label de la GUI,
        hace el reconociemiento del color y se le indica la posicion del 
        objeto reconocido para despues enviar esa informacion al servidor.
        
        """

        global prioridadBotones
        global move
        self.q = q
        
        # Tomamos una captura desde la webcam y la convertimos de BGR -> HSV.
        _,ipl_image = self.webcam.read()
        hsv = cv2.cvtColor(ipl_image, cv2.COLOR_BGR2HSV)

        # Establecemos el rango de colores que vamos a detectar
        # En este caso de verde oscuro a verde-azulado o claro
        verde_bajos = np.array([49,50,50], dtype=np.uint8)
        verde_altos = np.array([80, 255, 255], dtype=np.uint8)
 
        # Crear una mascara con solo los pixeles dentro del rango de verdes
        mask = cv2.inRange(hsv, verde_bajos, verde_altos) 

        # Encontrar el area de los objetos que detecta la camara
        moments = cv2.moments(mask)
        area = moments['m00']
 
        # Ver el area por pantalla
        #print area
        
        if(connection == True and area > 2000000):
         
                # Buscamos el centro x, y del objeto
                x = int(moments['m10']/moments['m00'])
                y = int(moments['m01']/moments['m00'])
         
                # Mostramos sus coordenadas por pantalla
                print "x = ", x
                print "y = ", y
            
                # Dibujamos una marca en el centro del objeto
                cv2.rectangle(ipl_image, (x, y), (x+2, y+2),(0,255,0), 2)

                # Posicionamiento del objeto y movimientos que realizara
                # Se mantiene en el sitio
                if (y>150 and y<300):
                    if (x>400): #Rota Derecha
                        move = "4"
                        print "Rota Derecha"

                    elif (x<200): #Rota Izquierda
                        move = "3"
                        print "Rota Izquierda"
                    
                    else: #Parado
                        move = "0"
                        print "Parado"

                #Atras
                elif (y>300):
                    if (x>400): #Atras-Derecha
                        move = "2"    
                        print "XCoordenadaMaximaX", x
                        print "Atras-Derecha"

                    elif (x<200): #Atras-Izquierda
                        move ="1"
                        print "XCoordenadaMinimaX", x
                        print "Atras-Izquierda"   
                    
                    else: #Atras
                        move = "8"
                        print "Atras"

                        if (y > 375): #Atras (a mayor velocidad)
                            move = "7"
                            print "Atras"
                            print "CoordenadaMaximaY"
              
                #Adelante
                elif (y<150):
                    if (x>400): #Adelante-Derecha
                        move = "6"
                        print "Adelante-Derecha"  

                    elif (x<200): #Adelante-Izquierda
                        move = "5"
                        print "Adelante-Izquierda"
                    
                    else: #Adelante
                        move = "9"
                        print "Adelante"

                        if (y < 75): #Adelante (a mayor velocidad)
                            move = "10"
                            print "Adelante"
                            print "CoordenadaMinimaY", y

        # Si no se observa objeto verde
        else:
            if (prioridadBotones):
                pass # No se realiza ninguna accion
                #print "prioridad a los botones" 
            else:
                move = "0" # Permance parado
                #print "Parado"
        if (connection == True):    
            clientSocket.send(move)


        # Creamos una imagen a partir de los datos.
        #
        # QImage
        # (
        #   Los pixeles que conforman la imagen,
        #   Ancho de de la imagen,
        #   Alto de de la imagen,
        #   Numero de bytes que conforman una linea (numero_de_bytes_por_pixels * ancho),
        #   Formato de la imagen
        # )
        image = QtGui.QImage(ipl_image.data, ipl_image.shape[1], ipl_image.shape[0], QtGui.QImage.Format_RGB888)

        # Creamos un pixmap a partir de la imagen.
        # OpenCV entraga los pixeles de la imagen en formato BGR en lugar del tradicional RGB,
        # por lo tanto tenemos que usar el metodo rgbSwapped() para que nos entregue una imagen con
        # los bytes Rojo y Azul intercambiados, y asi poder mostrar la imagen de forma correcta.
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        #Monstramos el pixmap en la QLable.
        self.MainWindow.lblWebcam.setPixmap(pixmap)
        

    #KeyboardControl Slots: 
    #funciones para el movimiento del robot a traves de los botones de la GUI.
    #Una vez que se pulsa un boton, se guarda del valor en la cola
    def pushUpKC(self):
        # Pulsado el boton UP
        q.put(ID_UP) 
        print "boton up pulsado"

    def pushDownKC(self):
        # Pulsado el boton DOWN
        q.put(ID_DOWN) 
        print "boton down pulsado"

    def pushLeftKC(self):
        # Pulsado el boton LEFT
        q.put(ID_LEFT) 
        print "boton left pulsado"

    def pushRightKC(self):
        # Pulsado el boton RIGHT
        q.put(ID_RIGHT) 
        print "boton right pulsado"

    def pushStopKC(self):
        # Pulsado el boton STOP
        q.put(ID_STOP) 
        print "boton stop pulsado"

    def establishConnection(self):
        # Pulsado el boton CONNECT 
        global connection 
        if (connection == False):
            print "Establishing Connection..."
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((sys.argv[1], 9999))
            print "Connected"
            self.connectKc.setEnabled(False)
            self.disconnectKc.setEnabled(True)
            self.exitKc.setEnabled(False)
            self.stopKC.setEnabled(True)
            self.upKC.setEnabled(True)
            self.downKC.setEnabled(True)
            self.leftKC.setEnabled(True)
            self.rightKC.setEnabled(True)
            connection = True
        
    def disconnection(self):
        # Pulsado el boton DISCONNECT
        global connection
        if (connection == True):
            print "Disconnected"
            clientSocket.send("Disconnect")
            clientSocket.close()
            self.connectKc.setEnabled(False)
            self.disconnectKc.setEnabled(False)
            self.exitKc.setEnabled(True)
            self.stopKC.setEnabled(False)
            self.upKC.setEnabled(False)
            self.downKC.setEnabled(False)
            self.leftKC.setEnabled(False)
            self.rightKC.setEnabled(False)
            connection = False

    def exitApplication(self):
        # Pulsado el boton EXIT
        self.MainWindow.close()


#--------------------------------------------------------------
# Clase KeyboardControl
#--------------------------------------------------------------
class KeyboardControlThread(threading.Thread):

    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q


    def run(self):
        """

        Esta funcion establece los parametros del movimiento
        del robot a traves de los botones. Estos valores son
        leidos de la cola, donde fueron almacenados mediante 
        los slots de la clase principal.
        
        """

        global f
        global prioridadBotones
        global move
        while True: 
            if not q.empty():
                obj = q.get(False)
                prioridadBotones=True

                if ID_UP==obj: # Se lee un valor ID_UP
                    if (move != ID_UP and move!=ID_UPP and move != ID_UPPP):
                        # Comprobamos que es la primera vez de forma consecutiva que se ha pulsado UP.
                        print "adelante: velocidad uno"
                        move= ID_UP
                    elif (move==ID_UP):
                        # Comprobamos que es la segunda vez consecutiva que se ha pulsado UP.
                        print "adelante: velocidad dos"
                        move = ID_UPP
                    elif (move == ID_UPP):
                        # Comprobamos que se ha pulsado UP por tercera o mas veces consecutivas.
                        print "adelante: velocidad tres"
                        move = ID_UPPP
                    
                elif ID_DOWN==obj: # Se lee un valor ID_DOWN
                    if (move != ID_DOWN and move!=ID_DOWNN and move != ID_DOWNNN):
                        # Comprobamos que es la primera vez de forma consecutiva que se ha pulsado DOWN.
                        print "atras: velocidad uno"
                        move= ID_DOWN
                    elif (move==ID_DOWN):
                        # Comprobamos que es la segunda vez consecutiva que se ha pulsado DOWN
                        print "atras: velocidad dos"
                        move = ID_DOWNN
                    elif (move == ID_DOWNN):
                        # Comprobamos que se ha pulsado DOWN por tercera o mas veces consecutivas.
                        print "atras: velocidad tres"
                        move = ID_DOWNNN

                elif ID_LEFT==obj: # Se lee un valor ID_LEFT
                        move=ID_LEFT                  
    
                elif ID_RIGHT==obj: # Se lee un valor ID_RIGHT
                        move=ID_RIGHT
 
                elif ID_STOP==obj: # Se lee un valor ID_STOP
                        prioridadBotones=False
                        move=ID_STOP                  
 
            else:
                time.sleep(0.1) 


#--------------------------------------------------------------
# Main
#--------------------------------------------------------------
if __name__ == "__main__":

    t = KeyboardControlThread(q)
    t.start()

    app = QtGui.QApplication(sys.argv)
    cliente_pfc = Cliente_pfc()
    cliente_pfc.MainWindow.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL) 

    app.exec_()