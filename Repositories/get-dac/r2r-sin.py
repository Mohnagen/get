import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

dac = None
try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.3, verbose=False)
    
    print(f"Генерация синусоиды: {signal_frequency} Гц, амплитуда: {amplitude} В")

    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        
        norm_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        
        voltage = amplitude * norm_amplitude
        
        dac.set_voltage(voltage)
        
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nГенерация прервана.")
finally:
    if dac:
        print("Сброс ЦАП и очистка GPIO")
        dac.deinit()