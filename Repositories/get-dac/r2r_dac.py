import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        
        if self.verbose:
            print("R2R DAC initialized.")
            print(f"  Pins (D0-D7): {self.gpio_bits}")
            print(f"  Dynamic Range: {self.dynamic_range:.2f} V")

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        if self.verbose:
            print("R2R DAC deinitialized and GPIO cleaned up.")

    def set_number(self, number):
        number = int(number)
        if not (0 <= number <= 255):
            print("Ошибка: Число должно быть в диапазоне от 0 до 255.")
            number = 0

        binary_string = bin(number)[2:].zfill(8)
        signal = [int(bit) for bit in binary_string]
        
        GPIO.output(self.gpio_bits, signal[::-1])
        
        if self.verbose:
            print(f"Число на выход: {number}, биты: {signal[::-1]}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за динамический диапазон (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)
        
        if self.verbose:
            print(f"Set voltage: {voltage:.2f} V -> Calculated number: {number}")
        
        self.set_number(number)

if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
        while True:
            try:
                input_str = input("Введите напряжение в Вольтах (или 'q' для выхода): ")
                if input_str.lower() == 'q':
                    break

                voltage = float(input_str)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
            except KeyboardInterrupt:
                print("\nПрограмма прервана пользователем.")
                break

    finally:
        if dac:
            dac.deinit()