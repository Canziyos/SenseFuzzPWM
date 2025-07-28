import time
from sensors.ultrasonic import Ultrasonic
from output.PWM import PWM
from sensors.pir import PIR
from fuzzy_logic.fuzzy_core import FuzzyCore
from fuzzy_logic.fuzzy_config import input_sets, output_sets, output_ranges, rules

controlller = FuzzyCore(input_sets, output_sets, rules, output_ranges)

# Ultrasonic sensor on pins 15 (trig) and 16 (echo).
#ultra = Ultrasonic(trig_pin=15, echo_pin=16)
pir = PIR(pin=17)

# Generic PWM output (buzzer or any PWM device) on pin 14
output_device = PWM(pin=14, mode="buzzer")
import time
from sensors.pir import PIR
from output.PWM import PWM
from fuzzy_logic.fuzzy_core import FuzzyCore
from fuzzy_logic.fuzzy_config import input_sets, output_sets, output_ranges, rules

# Initialize fuzzy controller.
controller = FuzzyCore(input_sets, output_sets, rules, output_ranges)

# PIR sensor on pin 17
pir = PIR(17)

# Generic PWM output (buzzer or any PWM device) on pin 14
output_device = PWM(pin=14, mode="buzzer")

# ======================
# Loooop....
# ======================
while True:
    # distance_mm = ultra.read()
    # if distance_mm is None:
    #     output_device.off()
    #     time.sleep(0.1)
    #print("Distance:", distance_mm, "mm")

    # Compute fuzzy outputs.
    # fuzzy_out = fuzzy_sonic.compute({"distance": distance_mm})
    fuzzy_out = controlller.compute({"motion: ", pir.read()})
    duty_percent = fuzzy_out["duty"]
    freq_hz = fuzzy_out["freq"]

    # Clamp frequency to safe range.
    freq_hz = min(max(100, freq_hz), 2000)

    # Update PWM output (continuous theremin mode).
    output_device.update(freq=freq_hz, duty=duty_percent)

    # Smooth update rate.
    time.sleep(0.1)