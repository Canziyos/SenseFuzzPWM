from machine import Pin, PWM

class PWM:
    def __init__(self, pin, mode="generic", freq=1000, duty=0):
        """
        Generic PWM controller.
        mode: 'buzzer', 'led', 'servo', or 'generic'
        freq: default frequency in Hz
        duty: initial duty in % (0-100)
        """
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin)
        self.mode = mode
        self.set_frequency(freq)
        self.set_duty(duty)

    def set_frequency(self, freq):
        # Clamp to safe MicroPython range
        freq = min(max(int(freq), 1), 20000)  # 1 Hz to 20 kHz
        self.pwm.freq(freq)

    def set_duty(self, duty_percent):
        # Clamp 0-100% and map to 0-65535
        duty_percent = min(max(duty_percent, 0), 100)
        self.pwm.duty_u16(int(duty_percent / 100 * 65535))

    def update(self, freq=None, duty=None):
        """
        Update both frequency and duty if provided.
        """
        if freq is not None:
            self.set_frequency(freq)
        if duty is not None:
            self.set_duty(duty)

    def off(self):
        """Stop output (set duty 0)"""
        self.pwm.duty_u16(0)

    def deinit(self):
        self.off()
        self.pwm.deinit()
