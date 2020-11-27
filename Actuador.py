#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib, urllib, requests
from time import sleep
import RPi.GPIO as GPIO
import time
import string
GPIO.setmode(GPIO.BCM)

pinMotor = 25

GPIO.setup(25, GPIO.OUT)

    while True:

   	baseURL = 'https://api.thingspeak.com/channels/1210618/fields/1/last' # xxxx = your channel id
	
        try:
		f = requests.get(baseURL)
		print f.text   #get data from url
		
                if f.text == '0':
                        GPIO.output(25, GPIO.HIGH) # motor off
                        print("motor off!!!")
                elif f.text == '1':
                        GPIO.output(25, GPIO.LOW)  # motor on
                        print ("motor on!!!")                
                else:
                        print ("not found command")
                	print '==========================================='  	
                	f.close()
            		sleep(5)
        except:
               print 'exit.'
               break;
        
