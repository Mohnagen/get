import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, led, dynamic_range, verbose = False):
        self.led = led
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.led, 0)
        GPIO.cleanup()  

    def set_number(self, number):
        bn = [int(element) for element in bin(number)[2:].zfill(8)]
        for i in range(len(self.led)):
            GPIO.output(self.led[i], bn[i])
        print(f'Число на выход ЦАП: {number}, биты: {bn}')

    def set_voltage(self, voltage):
        if not(0.0 <= voltage <= self.dynamic_range):
            print(f'Напряжение выходит за динамический диапазон ЦАП (0ю00 - {dynamic_range:.2f} В)')
            print(f'Устанавливаем 0.0 В') 
            self.set_number(0)
        self.set_number(int(voltage / self.dynamic_range * 255))


if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.15)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError():
                print("Вы ввели не число Попробуйте ещё раз")

    finally:
        dac.deinit() 