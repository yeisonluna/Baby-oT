#---------------------------------------------Baby-oT-----------------------------------------#
#-----------------------------------Pontificia Universidad Javeriana--------------------------#
#--------------------------------- --IoT: Fundamentos y Aplicaciones--------------------------#
#---------------------------Laura Aristizabal, Lorena Contreras y Yeison Luna-----------------#

#--------------------------Importación de bibliotecas-----------------------------------------#
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from datetime import datetime
#--------------------------Fin de importación de bibliotecas----------------------------------#


#--------------------Inicialización de variables y setup de GPIO------------------------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pinTemperatura = 23
pinMovimiento = 27
pinSonido = 4
pinLEDmov = 17

GPIO.setup(pinMovimiento, GPIO.IN)   #Pin del sensor de movimiento
GPIO.setup(pinSonido,GPIO.IN)
GPIO.setup(pinLEDmov, GPIO.OUT)  #LED output pin

now = datetime.now()
sensorTemp = Adafruit_DHT.DHT11
datos_bebe = {'Año':[],'Mes':[],'Dia':[],'Hora':[],'Temperatura':[],'Humedad':[],'EstadoCuna':[],'EstadoSonido':[]}
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


#--------------------Función tomaMovimiento----------------------------------------------------#          
def tomaMovimiento(pin,pin_led):    
    if(GPIO.input(pin)==False):                #Si el pin del sensor está en False o 0
        estado = "Tu bebé no está en la cuna"  #La variable estado notifica que el bebé no está
        GPIO.output(pin_led, 0)                #Apaga el LED
        
    elif(GPIO.input(pin)==True):               #En cambio si el pin del sensor está en 1
        estado = "Tu bebé está en la cuna"     #La variable estado notifica que el bebé está
        GPIO.output(pin_led, 1)                #Enciende el LED
    return estado
 #--------------------Fin Función tomaMovimiento-----------------------------------------------#  
    
    
#-------------------Fin Creación de funciones de toma de datos de los sensores-----------------#    

#------------------------ Inicio del ciclo infinito -------------------------------------------#
while True:                              #Siempre se encuentra dentro del ciclo
    
    datos_bebe['Año'].append(now.year)       #Se añade al diccionario de datos el año actual
    datos_bebe['Mes'].append(now.month)      #Se añade al diccionario de datos el mes actual
    datos_bebe['Dia'].append(now.day)        #Se añade al diccionario de datos el dia actual
    datos_bebe['Hora'].append([now.hour,now.minute]) #Se añade al diccionario la hora actual
    
    temp,hum = tomaTemperatura(sensorTemp,pinTemperatura)  #En las variables temp y hum se guardan
                                                           #temperatura y humedad, respectivamente
    datos_bebe['Temperatura'].append(temp)  #Se añade al diccionario de datos la temp. actual
    datos_bebe['Humedad'].append(hum)     #Se añade al diccionario de datos la humedad actual

    est_cuna = tomaMovimiento(pinMovimiento,pinLEDmov) #Se guarda el estado de movimiento del bebé
    datos_bebe['EstadoCuna'].append(est_cuna) #Se añade al diccionario de datos el estado de mov
    
    
    if(tomaSonido(pinSonido)):                   #Si el bebé llora o emite un sonido
        est_sonido = "¡Tu bebé te necesita!"     #Se notifica que el bebé requiere algo
    else:                                        #Si no
        est_sonido = "Tu bebé está en silencio"  #Se notifica que el bebé está en silencio
        
    datos_bebe['EstadoSonido'].append(est_sonido) #Se añade al diccionario de datos el estado de
                                                  #sonido
    
    for key in datos_bebe:                       #Impresión en pantalla del diccionario
        print(key,":",datos_bebe[key])
    print("\n")
#--------------------------Fin del ciclo-------------------------------------------------------#

#--------------------------Fin del programa-----------------------------------------------------#
