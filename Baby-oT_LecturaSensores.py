import Adafruit_DHT
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pinTemperatura = 23
pinMovimiento = 27
pinSonido = 4
pinLEDmov = 17

GPIO.setup(pinMovimiento, GPIO.IN)   #Pin del sensor de movimiento
GPIO.setup(pinSonido,GPIO.IN)
GPIO.setup(pinLEDmov, GPIO.OUT)  #LED output pin

sensorTemp = Adafruit_DHT.DHT11
cont_llora = 0

    
def tomaTemperatura(sensor,pin):
    humedad, temperatura = Adafruit_DHT.read_retry(sensor,pin)
    #Se implementa cadenas f de python para imprimir con variables -- 2f significa con dos decimales
    if humedad is not None and temperatura is not None:
        print(f'Temperatura={temperatura:.2f}*C Humedad={humedad:.2f}%')
        #print("Temperatura = {}".format((temperatura))  ---> otra manera de imprimir
    else:
        print('Falló la lectura del sensor. Intentar de nuevo')
        

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
        print("Tu bebé no está en la cuna")
        GPIO.output(pin_led, 0)  #Turn OFF LED
        
    elif(GPIO.input(pin)==True):       #When output from motion sensor is HIGH
        print("Tu bebé está en la cuna")
        GPIO.output(pin_led, 1)  #Turn ON LED
        

while True:
    
    tomaTemperatura(sensorTemp,pinTemperatura)
    tomaMovimiento(pinMovimiento,pinLEDmov)
    
    if(tomaSonido(pinSonido)):
        print("¡Tu bebé te necesita!")
        #cont_llora+=1
    #if(cont_llora > 2):
        #print("¡Tu bebé te necesita!")
        #cont_llora = 0
    else:
        print("Tu bebé está en silencio")
    
      
    

    
    

        
