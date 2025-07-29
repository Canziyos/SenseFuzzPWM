import time
from input.sensors import Ultrasonic, PIR
from input.interaction import MotionDistanceManager
from output.pwm import PWM
from fuzzy_logic.fuzzy_core import FuzzyCore
from fuzzy_logic.fuzzy_config import input_sets, output_sets, output_ranges, rules

# Initialize fuzzy controller.
try:
    controller = FuzzyCore(input_sets, output_sets, rules, output_ranges)
except Exception as e:
    print("FuzzyCore init error:", e)
    controller = None

# Initialize sensors.
try:
    pir = PIR(17)  # PIR on GPIO 17.
except Exception as e:
    print("PIR init error:", e)
    pir = None

try:
    ultra = Ultrasonic(trig_pin=15, echo_pin=16)  # Ultrasonic on GPIO 15/16.
except Exception as e:
    print("Ultrasonic init error:", e)
    ultra = None

# Manager to handle PIR/Ultrasonic interaction.
try:
    manager = MotionDistanceManager(pir, ultra, active_ms=60000)
except Exception as e:
    print("Manager init error:", e)
    manager = None

# Generic PWM output (buzzer or any PWM device) on pin 14.
try:
    output_device = PWM(pin=14, mode="buzzer")
except Exception as e:
    print("PWM init error:", e)
    output_device = None

# ======================
# Loooop....
# ======================
while True:
    try:
        if not manager or not controller or not output_device:
            print("Critical init failed, waiting...")
            time.sleep(1)
            continue

        active, distance_mm = manager.update()

        if active and distance_mm is not None:
            # Compute fuzzy outputs (distance only; PIR used as gate).
            fuzzy_out = controller.compute({"distance": distance_mm})
            duty_percent = fuzzy_out["duty"]
            freq_hz = fuzzy_out["freq"]

            # Clamp frequency to safe range.
            freq_hz = min(max(100, freq_hz), 2000)

            # Update PWM output.
            output_device.update(freq=freq_hz, duty=duty_percent)

        else:
            # Silence output if inactive or no valid distance.
            output_device.off()

        time.sleep(0.1)

    except Exception as e:
        # Catch any runtime errors to prevent crash loop.
        print("Main loop error:", e)
        if output_device:
            output_device.off()
        time.sleep(0.5)
