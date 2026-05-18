import signal_triangle as sg
import time
import pwm_dac as pwm

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

if __name__ == '__main__':
    try:
        dac = pwm.PWM_DAC(12, 500, 3.3, True)
        start = time.time()
        
        while True:
            current = time.time() - start
            dac.set_voltage(amplitude * sg.get_triangle(signal_frequency, current))
            sg.wait_for_sampling_period(sampling_frequency)
        
    finally:
        dac.deinit()