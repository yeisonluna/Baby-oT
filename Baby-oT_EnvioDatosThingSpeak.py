#---------------------------------------------Baby-oT-----------------------------------------#
#-----------------------------------Pontificia Universidad Javeriana--------------------------#
#--------------------------------- --IoT: Fundamentos y Aplicaciones--------------------------#
#---------------------------Laura Aristizabal, Lorena Contreras y Yeison Luna-----------------#

#--------------------------Importación de bibliotecas-----------------------------------------#
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from datetime import datetime
import spidev
from numpy import interp
from time import sleep
import paho.mqtt.publish as publish
import time
import requests
import string
#--------------------------Fin de importación de bibliotecas----------------------------------#


#--------------------Inicialización de variables y setup de GPIO------------------------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setmode(GPIO.BCM)

pinTemperatura = 23
pinMovimiento = 27
pinSonido = 4
pinMotor = 26


GPIO.setup(pinMovimiento, GPIO.IN)   #Pin del sensor de movimiento
GPIO.setup(pinSonido,GPIO.IN)
GPIO.setup(pinMotor,GPIO.OUT)


now = datetime.now()
sensorTemp = Adafruit_DHT.DHT11

# Creacion topic para envio a ThingSpeak usando protocolo MQTT
topic='channels/'+str(1210618)+'/publish/'+str('J3YZTZYWGGVSNCP7')
mqttHost = 'mqtt.thingspeak.com'

#--------------------Fin Inicialización de variables y setup de GPIO---------------------------#


#--------------------Creación de funciones de toma de datos de los sensores--------------------#


#--------------------Función tomaTemperatura---------------------------------------------------#
def tomaTemperatura(sensor,pin):
    humedad, temperatura = Adafruit_DHT.read_retry(sensor,pin) #Se utiliza libreria AdafruitDHT
    if humedad is not None and temperatura is not None: #Si hay datos en el sensor, entonces
                                                        #se asignan a las variables a y b
        a = temperatura        
        b = humedad
    else:
        print('Falló la lectura del sensor. Intentar de nuevo') #Si no hay datos, se notifica
    return a,b   #Retorna temperatura y humedad
 #--------------------Fin Función tomaTemperatura----------------------------------------------#  
    

#--------------------Función tomaSonido--------------------------------------------------------#    
def tomaSonido(pin):    
    if(GPIO.input(pin)==True):   #Si hay un valor verdadero en el pin del sensor, se asigna True
        bebe_llora = True        #a la variable bebe_llora
    else:
        bebe_llora = False      #De lo contrario, bebe_llora es False
    return bebe_llora
#--------------------Fin Función tomaSonido----------------------------------------------------# 

#--------------------Función analogInput-------------------------------------------------------#    
def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3)<<8)+adc[2]
    return data
#--------------------Fin Función analogInput---------------------------------------------------# 

#--------------------Función tomaMovimiento----------------------------------------------------#          
def tomaMovimiento(pin):    
    if(GPIO.input(pin)==False):                #Si el pin del sensor está en False o 0
        estado = 0  #La variable estado notifica que el bebé no está
    
        
    elif(GPIO.input(pin)==True):               #En cambio si el pin del sensor está en 1
        estado = 1     #La variable estado notifica que el bebé está
    return estado
 #--------------------Fin Función tomaMovimiento-----------------------------------------------#  
    
    
#-------------------Fin Creación de funciones de toma de datos de los sensores-----------------#  




#------------------------ Inicio del ciclo infinito -------------------------------------------#
while True:
    
    baseURL = 'https://api.thingspeak.com/channels/1244148/fields/1/last'
    sonido = analogInput(0)
    sonido = interp(sonido,[0,1023],[0,100])
    movimiento = tomaMovimiento(pinMovimiento) #Se guarda el estado de movimiento del bebé
    temperatura,humedad = tomaTemperatura(sensorTemp,pinTemperatura)  
    payload='field1='+str(temperatura)+'&field2='+str(humedad)+'&field3='+str(sonido)+'&field4='+str(movimiento)

    try:
        publish.single(topic, payload, hostname=mqttHost)
        f = requests.get(baseURL)
        print(f.text)   #get data from url
            
        if f.text == '0':
            GPIO.output(pinMotor,0) # motor off
            print("motor off!!!")
        elif f.text == '1':
            GPIO.output(pinMotor,1)  # motor on
            print ("motor on!!!")                
        else:
            print("not found command")
            print('===========================================')  
            f.close()
       
    except:
        print("except: problemas envio datos MQTT y actuador")
        break
   
    sleep(15)    
#--------------------------Fin del ciclo-------------------------------------------------------#

#--------------------------Fin del programa-----------------------------------------------------#