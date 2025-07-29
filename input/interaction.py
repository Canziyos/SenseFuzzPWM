# input/interaction.py
from time import ticks_ms

class MotionDistanceManager:
    def __init__(self, pir_sensor, distance_sensor, active_ms=60000):
        self.pir = pir_sensor
        self.distance = distance_sensor
        self.active_ms = active_ms
        self.state = "IDLE"
        self.last_motion = 0  # last time PIR was HIGH

    def update(self):
        """
        Returns:
          - active (bool): should fuzzy logic run?
          - distance (mm or None): current distance (if active)
        """
        now = ticks_ms()
        pir_value = self.pir.read()

        # --- STATE LOGIC ---
        if self.state == "IDLE":
            if pir_value == 1:  # Motion detected
                self.state = "ACTIVE"
                self.last_motion = now

        elif self.state == "ACTIVE":
            if pir_value == 1:
                self.last_motion = now  # refresh active window.
            elif now - self.last_motion > self.active_ms:
                self.state = "IDLE"  # 1 min expired.
    

        # --- OUTPUT ---
        active = self.state == ("ACTIVE")
        distance = self.distance.read() if active else None
        return active, distance
