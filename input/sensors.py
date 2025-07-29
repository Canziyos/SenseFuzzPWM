from machine import Pin, time_pulse_us
from time import sleep_us, ticks_ms

class Ultrasonic:
    def __init__(self, trig_pin, echo_pin, max_distance_mm=2000, samples=3):
        """
        Ultrasonic distance sensor.
        trig_pin, echo_pin: GPIO numbers
        max_distance_mm: maximum measurable distance (beyond = None)
        samples: number of readings to average for smoothing
        """
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.max_distance_mm = max_distance_mm
        self.samples = samples

    def _single_read(self):
        """Perform one ultrasonic measurement (raw)."""
        # Trigger pulse
        self.trig.low()
        sleep_us(2)
        self.trig.high()
        sleep_us(10)
        self.trig.low()

        # Measure echo
        pulse = time_pulse_us(self.echo, 1, 30_000)  # timeout 30ms
        if pulse < 0:
            return None
        dist = int(pulse * 0.1715)  # mm
        if dist > self.max_distance_mm:
            return None
        return dist

    def read(self):
        """
        Return averaged distance in mm (or None if no valid reading).
        """
        readings = []
        for _ in range(self.samples):
            d = self._single_read()
            if d is not None:
                readings.append(d)
            sleep_us(1000)  # small delay between samples
        return int(sum(readings) / len(readings)) if readings else None


class PIR:
    def __init__(self, sense_pin, warmup_ms=30000):
        """
        PIR motion sensor (digital).
        sense_pin: GPIO number
        warmup_ms: ignore readings for this duration after power-up
        """
        self.sense = Pin(sense_pin, Pin.IN)
        self.warmup_ms = warmup_ms
        self.start_time = ticks_ms()

    def read(self):
        """
        Return 0 or 1 after warm-up period.
        Before warm-up expires, always return 0.
        """
        if ticks_ms() - self.start_time < self.warmup_ms:
            return 0
        return self.sense.value()
