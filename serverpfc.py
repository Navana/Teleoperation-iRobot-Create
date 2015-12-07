#!/usr/bin/env python

"""

Filename: sesrverpfc.py

Description: Contiene la clase Server y, como su propio nombre indica,
es la parte servidor de la aplicacion. Recibe las ordenes del cliente 
y, en funcion de las mismas, las procesa y hace que el robot ejecute
los movimientos gracias al servicio tank del driver irobot_create_2_1.

"""

import sys
import signal # Modulo que proporciona mecanismos de gestion de eventos asincronos del sistema.

#Cargamos modulos de ROS
import roslib; roslib.load_manifest('irobot_create_2_1')
import rospy

#Cargamos modulos de iRobot
from irobot_create_2_1.msg import SensorPacket
from irobot_create_2_1.srv import *

#Cargamos otras librerias
from std_msgs.msg import Empty
import Queue
import time
import socket
from time import sleep

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
f = None

rospy.wait_for_service('tank') # Instruccion de bloqueo; espera que el servicio 'tank' este disponible.
f = rospy.ServiceProxy('tank',Tank) #Inicializa el servicio 'tank' del driver.


#--------------------------------------------------------------
# Clase Server
#--------------------------------------------------------------
class Server:

    def connect():
        """

        Esta funcion abre la conexion al cliente. La informacion que este
        le envie, es tratada a traves de una peticion por el servicio 
        'tank', que lo ejecuta. 
        
        """

        #Creamos el socket y establecemos el puerto correspondiente.
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 9999
        print "server active"

        #Invoco  al metodo bind, pasando como parametro una tupla con IP 
        # y puerto
        serverSocket.bind(('', port))

        #Invoco  el metodo listen para escuchar conexiones con el numero 
        # maximo de conexiones como parametro; en este caso, 1.
        serverSocket.listen(1)

        #El metodo accept bloquea la ejecucion a la espera de conexiones 
        # accept devuelve un objeto socket y una tupla IP y puerto
        clientSocket, addr = serverSocket.accept()

        # Inicializacion de variables
        leftSpeed = 0
        rightSpeed = 0
        changeSpeed = 50

        while True:
            # Instruccion bloqueante. Se recibe un stream en el socket con
            # un maximo de 1024 bytes.
            receivedData = clientSocket.recv(1024)

            # Tratamiento del dato recibido

            if (receivedData == "Disconnect"): # Desconexion
                print "Disconnecting"
                # Cierra los sockets que se han creado y finaliza el proceso.
                serverSocket.close
                clientSocket.close
                break

            
            elif (receivedData=="0"): #Parado
                leftSpeed = 0
                rightSpeed = 0
                f(False, leftSpeed, rightSpeed) # Ejecucion del servicio 'tank'.
                                                # Esta opecarion se repetira en
                                                # todos los posibles casos de 
                                                #recepcion del dato.
                #print "Parado", self.leftSpeed, self.rightSpeed

            elif (receivedData=="1"): #Atras-Izquierda
                leftSpeed = -50
                rightSpeed = -125
                f(False, leftSpeed, rightSpeed) 
                print "Atras-Izquierda", leftSpeed, rightSpeed  

            elif (receivedData=="2"): #Atras-Derecha
                leftSpeed = -125
                rightSpeed = -50
                f(False, leftSpeed, rightSpeed)
                print "Atras-Derecha", leftSpeed, rightSpeed 

            elif (receivedData=="3"): #Rota Izquierda
                leftSpeed = -100
                rightSpeed = 100
                f(False, leftSpeed, rightSpeed)
                print "Rota Izquierda", leftSpeed, rightSpeed  
       
            elif (receivedData=="4"): #Rota Derecha
                leftSpeed = 100
                rightSpeed = -100
                f(False, leftSpeed, rightSpeed)
                print "Rota Derecha", leftSpeed, rightSpeed 

            elif (receivedData=="5"): #Adelante-Izquierda
                leftSpeed = 50
                rightSpeed = 125
                f(False, leftSpeed, rightSpeed)
                print "Adelante-Izquierda", leftSpeed, rightSpeed  
    
            elif (receivedData=="6"): #Adelante-Derecha
                leftSpeed = 125
                rightSpeed = 50
                f(False, leftSpeed, rightSpeed)
                print "Adelante-Derecha", leftSpeed, rightSpeed 

            elif (receivedData=="7"): #Atras (a mayor velocidad)
                leftSpeed = -125
                rightSpeed = -125
                f(False, leftSpeed, rightSpeed)
                print "Atras", leftSpeed, rightSpeed

            elif (receivedData=="8"): #Atras
                leftSpeed = -50
                rightSpeed = -50
                f(False, leftSpeed, rightSpeed)
                print "Atras", leftSpeed, rightSpeed

            elif (receivedData=="9"): #Adelante
                leftSpeed = 50
                rightSpeed = 50           
                f(False, leftSpeed, rightSpeed)
                print "Adelante", leftSpeed, rightSpeed

            elif (receivedData=="10"): #Adelante (a mayor velocidad)
                leftSpeed = 125
                rightSpeed = 125
                f(False, leftSpeed, rightSpeed)
                print "Adelante", leftSpeed, rightSpeed

            elif (receivedData==ID_STOP):
                try:
                    leftSpeed=0
                    rightSpeed=0
                    f(False, 0, 0)
                except:
                    f(False,0,0)

            elif (receivedData==ID_UP):
                print "Arriba", receivedData
                f(False, 50, 50)
                leftSpeed = 50
                rightSpeed = 50
            
            elif (receivedData==ID_UPP):
                leftSpeed = 3*changeSpeed
                rightSpeed = 3*changeSpeed
                f(False, leftSpeed, rightSpeed)
            
            elif (receivedData==ID_UPPP):
                leftSpeed = 5*changeSpeed
                rightSpeed = 5*changeSpeed
                f(False, leftSpeed, rightSpeed)

            elif (receivedData==ID_DOWN):
                print "Abajo", receivedData
                f(False, -50, -50)
                leftSpeed = -50
                rightSpeed = -50

            elif (receivedData==ID_DOWNN):
                print "Aabajo", receivedData
                leftSpeed = -3*changeSpeed
                rightSpeed = -3*changeSpeed
                f(False, leftSpeed, rightSpeed)

            elif (receivedData==ID_DOWNNN):
                print "Aaabajo", receivedData
                leftSpeed = -5*changeSpeed
                rightSpeed = -5*changeSpeed
                f(False, leftSpeed, rightSpeed)

            elif (receivedData==ID_LEFT):
                print "Izquiera", receivedData
                try:
                    if leftSpeed < 500 and rightSpeed <500:
                        leftSpeed += 2*changeSpeed
                        rightSpeed += 2*changeSpeed
                        f(False, -100, 100)
                except:
                    f(False,0,0)
       
            elif (receivedData==ID_RIGHT):
                print "Derecha", receivedData
                try:
                    if leftSpeed > -500 and rightSpeed >-500:
                        leftSpeed -= 2*changeSpeed
                        rightSpeed -= 2*changeSpeed
                        f(False, 100, -100)
                except:
                    f(False,0,0)

            # Si no se observa objeto verde o no se recibe nada. 
            # Esto no implica que este desconectado.
            else:
                leftSpeed = 0
                rightSpeed = 0
                f(False, leftSpeed, rightSpeed)
   
    connect()