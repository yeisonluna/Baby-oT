#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib, urllib, requests
from time import sleep
import RPi.GPIO as GPIO
import time
import string
GPIO.setmode(GPIO.BOARD)

led1 = 11
led2 = 13
led3 = 15

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

def main():

    while True:

   	baseURL = 'https://api.thingspeak.com/channels/xxxx/fields/1/last' # xxxx = your channel id
	
        try:
		f = requests.get(baseURL)
		print f.text   #get data from url
		
                if f.text == '10':
                        GPIO.output(11, GPIO.HIGH) # led 1 off
                        print("led 1 off!!!")
                elif f.text == '11':
                        GPIO.output(11, GPIO.LOW)  # led 1 on
                        print ("led 1 on!!!")
                elif f.text == '20':
                        GPIO.output(13, GPIO.HIGH) # led 2 off
                        print("led 2 off!!!")
                elif f.text == '21':
                        GPIO.output(13, GPIO.LOW) # led 2 on
                        print("led 2 on!!!")
                elif f.text == '30':
                        GPIO.output(15, GPIO.HIGH) # led 3 off
                        print("led 3 off!!!")
                elif f.text == '31':
                        GPIO.output(15, GPIO.LOW) # led 3 on
                        print("led 3 on!!!")
                elif f.text == '777':             # turn off all LED
                        GPIO.output(11, GPIO.HIGH)
                        GPIO.output(13, GPIO.HIGH)
                        GPIO.output(15, GPIO.HIGH)
                        print("LED off all !!!")
                elif f.text == '999':             # turn on all LED   
                        GPIO.output(11, GPIO.LOW)
                        GPIO.output(13, GPIO.LOW)
                        GPIO.output(15, GPIO.LOW)
                        print("LED on all !!!")
                else:
                        print ("not found command")
                	print '==========================================='  	
                	f.close()
            		sleep(5)
        except:
               print 'exit.'
               break;
        
