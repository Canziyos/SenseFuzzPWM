from machine import Pin

class PIR:
    def __init__(self, sense_pin):
        self.sense = Pin(sense_pin, Pin.IN)



    def read(self):
        return self.sense.value()