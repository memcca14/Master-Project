'''
**********************************************************************
* Filename    : dht11.py
* Description : test for SunFoudner DHT11 humiture & temperature module
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-30    New release
**********************************************************************
'''


#TESTING NOTES
#TAKES INPUTS FROM HUMIDITURE AND PRINTS
#WHEN TOUCHING WATER PRINT "water detected!" AND STARTS BUZZER
#BUZZER WILL STOP ONCE HUMIDITY IS LOW ENOUGH ONCE MORE
#ONLY COMPLAINT IS AN ODD TICKING NOISE.

#imports
import RPi.GPIO as GPIO
import time

#buzzer setup
Buzzer = 27  # Pin for the buzzer


CL = [0, 131, 147, 165, 175, 196, 211, 248]      # Frequency of Low C notes
CM = [0, 262, 294, 330, 350, 393, 441, 495]      # Frequency of Middle C notes
CH = [0, 525, 589, 661, 700, 786, 882, 990]      # Frequency of High C notes

song_1 = [   CM[3], CM[5], CM[6]   ]

beat_1 = [   1, 1, 3, 1, 1, 3, 1, 1,         # Beats of song 1, 1 means 1/8 beats
            1, 1, 1, 1, 1, 1, 3, 1,
            1, 3, 1, 1, 1, 1, 1, 1,
            1, 2, 1, 1, 1, 1, 1, 1,
            1, 1, 3    ]

def setup():
	GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
	global Buzz                        # Assign a global variable to replace GPIO.PWM
	Buzz = GPIO.PWM(Buzzer, 1)    # 440 is the initial frequency.
	Buzz.start(50)                    # Start Buzzer pin with 50% duty ratio
	
    
def activate_buzzer():
    # Play a simple song 
		for i in range(1, len(song_1)):
			Buzz.ChangeFrequency(song_1[1])
			time.sleep(beat_1[i] * 0.5)

#humiditure setup
#!/usr/bin/env python3

DHTPIN = 17

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

def read_dht11_dat():
	GPIO.setup(DHTPIN, GPIO.OUT)
	GPIO.output(DHTPIN, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHTPIN, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHTPIN)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		#print ("Data not good, skip")
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	#print ("bits: %s, length: %d" % (bits, len(bits)))
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	#print (the_bytes)
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		#print ("Data not good, skip")
		return False

	return the_bytes[0], the_bytes[2]

def main():
	print ("Raspberry Pi wiringPi DHT11 Temperature test program\n")
	setup() #set up buzzer
	while True:
		result = read_dht11_dat()
		if result:
			humidity, temperature = result
			print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
			if humidity > 60:
				print ("water detected!")
				activate_buzzer()
			else:
				Buzz.ChangeFrequency(1)
			time.sleep(1)

def destroy():
	Buzz.stop()
	GPIO.output(Buzzer, 1)        # Set Buzzer pin to High
	GPIO.cleanup()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		destroy() 
