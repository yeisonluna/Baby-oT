import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from datetime import datetime


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
cont_llora = 0
datos_bebe = {'Año':[],'Mes':[],'Dia':[],'Hora':[],'Temperatura':[],'Humedad':[],'EstadoCuna':[],'EstadoSonido':[]}

    
def tomaTemperatura(sensor,pin):
    humedad, temperatura = Adafruit_DHT.read_retry(sensor,pin)
    if humedad is not None and temperatura is not None:
        #print(f'Temperatura={temperatura:.2f}*C Humedad={humedad:.2f}%')
        a = temperatura
        b = humedad
    else:
        print('Falló la lectura del sensor. Intentar de nuevo')
    return a,b
        

def tomaSonido(pin):
    if(GPIO.input(pin)==True):
        bebe_llora = True
        #print("sonido")
    else:
        bebe_llora = False
        #print("silencio")
    return bebe_llora

        
def tomaMovimiento(pin,pin_led):    
    if(GPIO.input(pin)==False): #When output from motion sensor is LOW
        estado = "Tu bebé no está en la cuna"
        GPIO.output(pin_led, 0)  #Turn OFF LED
        
    elif(GPIO.input(pin)==True):       #When output from motion sensor is HIGH
        estado = "Tu bebé está en la cuna"
        GPIO.output(pin_led, 1)  #Turn ON LED
    return estado
        

while True:
    
    datos_bebe['Año'].append(now.year)
    datos_bebe['Mes'].append(now.month)
    datos_bebe['Dia'].append(now.day)
    datos_bebe['Hora'].append([now.hour,now.minute])
    
    temp,hum = tomaTemperatura(sensorTemp,pinTemperatura)    
    datos_bebe['Temperatura'].append(temp)
    datos_bebe['Humedad'].append(hum)

    est_cuna = tomaMovimiento(pinMovimiento,pinLEDmov)
    datos_bebe['EstadoCuna'].append(est_cuna)
    
    
    if(tomaSonido(pinSonido)):
        est_sonido = "¡Tu bebé te necesita!"
    else:
        est_sonido = "Tu bebé está en silencio"
        
    datos_bebe['EstadoSonido'].append(est_sonido)
    
    for key in datos_bebe:
        print(key,":",datos_bebe[key])
