import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range

        if self.verbose:
            print("ЦАП MCP4725 инициализирован.")
            print(f"  I2C Адрес: 0x{self.address:02X}")
            print(f"  Динамический диапазон: {self.dynamic_range:.2f} В")

    def deinit(self):
        self.set_number(0)
        self.bus.close()
        if self.verbose:
            print("ЦАП MCP4725 деинициализирован. Шина I2C закрыта.")

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
            
        number = int(number)
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит, 0-4095)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
            
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за динамический диапазон (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0
        
        number = int(voltage / self.dynamic_range * 4095)
        
        self.set_number(number)

if __name__ == "__main__":
    dac = None
    try:
        dac = MCP4725(dynamic_range=3.3, address=0x61, verbose=True)
        
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