#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 12
Buzzer = 11

def setup_distance_sensor():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

 def setup_active_buzzer(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, GPIO.HIGH)
	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def on_buzzer():
	GPIO.output(BuzzerPin, GPIO.LOW)

def off_buzzer():
	GPIO.output(BuzzerPin, GPIO.HIGH)

def beep_buzzer(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

def loop_buzzer():
	while True:
		beep(0.5)

def destroy_buzzer():
	GPIO.output(BuzzerPin, GPIO.HIGH)
	GPIO.cleanup() 


def loop_distance():
	while True:
		dis = distance()
		print (dis, 'cm')
		print ('')
		time.sleep(0.3)

def destroy_distance():
	GPIO.cleanup()

if __name__ == "__main__":
	setup_distance_sensor()
        setup(Buzzer)
	try:
		loop_distance()
                loop_buzzer()
	except KeyboardInterrupt:
		destroy_distance()
                destroy_buzzer()



		
