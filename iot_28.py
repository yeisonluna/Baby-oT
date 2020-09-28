# -*- coding: utf-8 -*-

# Codigo Yeison Luna

import requests

#Ingreso variables

codigo = float(input("Ingrese codigo: "))
nombre = input("Ingrese nombre: ")
apellido = input("Ingrese apellido ")

def sumar(code):
    code=code+1000
    return code
    
def multiplicar(code):
    code=code*2
    return code

suma = sumar(codigo)
multiplicacion = multiplicar(codigo)

resultado = multiplicacion - suma

enviar = requests.get("https://api.thingspeak.com/update?api_key=XWPAK9IHIKQ3KFZ9&field1="+nombre+"&field2="+apellido+"&field3="+str(resultado))





