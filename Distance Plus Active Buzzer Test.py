# buzzer code 
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

Buzzer = 11    # pin11

def setupB(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, GPIO.HIGH)

def on():
	GPIO.output(BuzzerPin, GPIO.LOW)

def off():
	GPIO.output(BuzzerPin, GPIO.HIGH)

def beep(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 12

def setupA():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def loop():
	while True:
		dis = distance()
		print (dis, 'cm')
		print ('')
		if dis <= 10:
		    beep(0.5)
		time.sleep(0.3)

def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH) #from buzzer code
	GPIO.cleanup()

if __name__ == "__main__":
	setupA() # set up distance sensor
	setupB(Buzzer) #set up buzzer
	try:
		loop()
	except KeyboardInterrupt:
		destroy()