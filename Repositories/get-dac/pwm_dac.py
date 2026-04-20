import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

        if self.verbose:
            print("PWM DAC initialized.")
            print(f"  Pin: {self.gpio_pin}")
            print(f"  PWM Frequency: {self.pwm_frequency} Hz")
            print(f"  Dynamic Range: {self.dynamic_range:.2f} V")

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()
        if self.verbose:
            print("PWM DAC deinitialized and GPIO cleaned up.")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за динамический диапазон (0.00 - {self.dynamic_range:.2f} В)")
            voltage = 0.0
            print("Устанавливаем 0.0 В")
        
        duty_cycle = (voltage / self.dynamic_range) * 100
        
        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Напряжение: {voltage:.2f} V -> Коэффициент заполнения: {duty_cycle:.1f}%")

if __name__ == "__main__":
    dac = None
    try:
        dac = PWM_DAC(12, 500, 3.290, True)
        
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