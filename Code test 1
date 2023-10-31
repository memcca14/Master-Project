import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 12
BuzzerPin = 13  # Use a different pin for the buzzer

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def beep(x):
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(x)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(x)

def loop():
    while True:
        dis = distance()
        print(dis, 'cm')

        if dis < 50:
            print("Buzzer activated!")
            beep(0.1)  # You can adjust the beep duration as needed

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
