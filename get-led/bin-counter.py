import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = list(reversed([24, 22, 23, 27, 17, 25, 12, 16]))
print(leds)

GPIO.setup(leds, GPIO.OUT)

GPIO.output(leds, 0)

up = 9
down = 10

GPIO.setup([up, down], GPIO.IN)

num = 0

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

sleep_time = 0.2

while True:
    if GPIO.input(up):
        num += 1
        num = min(num, 2 ** 8 - 1)
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(down):
        num -= 1
        num = max(0, num)
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    for i in range(len(leds)):
        if dec2bin(num)[i] == 1:
            GPIO.output(leds[i], 1)
        if dec2bin(num)[i] == 0:
            GPIO.output(leds[i], 0)
