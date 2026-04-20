import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
dac_bits = [22,27,17,26,25,21,20,16]
GPIO.setup(dac_bits, GPIO.OUT)
dynamic_range = float(3.3)
def voltage_to_number(voltage):
    if not ( 0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за данимический диапозон ЦАП (0.00 - {dynamic_range: .2f} 2B)")
        print("устанавливаем 0.0В")
        return 0
    return int((voltage / dynamic_range) * 255)

def number_to_dac(number):
    return [int(i) for i in bin(number)[2:].zfill(8)]

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в вольтах"))
            number = voltage_to_number(voltage)
            out = number_to_dac(number)[::-1]
            print("Вывод ЦАП:" ,out)
            for i in range(8):
                GPIO.output(dac_bits[i],out[i])
        except ValueError:
            print("Вы ввели не число, введите еще раз")
finally:
    GPIO.output(dac_bits,0)
    GPIO.cleanup()