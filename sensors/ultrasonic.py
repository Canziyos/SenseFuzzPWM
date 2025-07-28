from machine import Pin, time_pulse_us
from time import sleep_us

class Ultrasonic:
    def __init__(self, trig_pin, echo_pin, max_distance_mm=2000):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.max_distance_mm = max_distance_mm

    def read(self):
        # Trigger pulse..
        self.trig.low()
        sleep_us(2)
        self.trig.high()
        sleep_us(10)
        self.trig.low()

        # Measure echo
        pulse = time_pulse_us(self.echo, 1, 30_000)  # timeout 30ms.
        if pulse < 0:
            return None
        dist = int(pulse * 0.1715)  # mm
        if dist > self.max_distance_mm:
            return None
        return dist