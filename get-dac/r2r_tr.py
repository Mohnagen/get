import r2r_dac as r2r
import signal_triangle as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


if __name__ == '__main__':
    try:
        dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.2, True)
        start = time.time()
        
        while True:
            current = time.time() - start
            dac.set_voltage(amplitude * sg.get_triangle(signal_frequency, current))
            sg.wait_for_sampling_period(sampling_frequency)
        
    finally:
        dac.deinit()