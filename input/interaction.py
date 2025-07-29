# input/interaction.py

from sensors import Ultrasonic, PIR
from time import ticks_ms

class MotionDistanceManager:
    def __init__(self, pir_sensor, distance_sensor, active_ms=60000, grace_ms=1000):
        self.pir = pir_sensor
        self.distance = distance_sensor
        self.active_ms = active_ms
        self.grace_ms = grace_ms

        self.state = "IDLE"
        self.last_motion = 0  # last time PIR was HIGH
        self.grace_start = 0

    def update(self):
        """
        Called repeatedly in main loop.
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
                self.last_motion = now  # refresh active window
            elif now - self.last_motion > self.active_ms:
                self.state = "IDLE"  # 1 min expired
            elif pir_value == 0:
                self.state = "GRACE"
                self.grace_start = now

        elif self.state == "GRACE":
            if pir_value == 1:
                self.state = "ACTIVE"  # back to active
                self.last_motion = now
            elif now - self.grace_start > self.grace_ms:
                self.state = "IDLE"  # confirmed no motion

        # --- OUTPUT ---
        active = self.state in ("ACTIVE", "GRACE")
        distance = self.distance.read() if active else None
        return active, distance
