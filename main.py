import time
from fuzzy_core import FuzzyCore
from membership import gaussian, triangular, trapezoidal
from ultrasonic import Ultrasonic
from PWMOutput import PWMOutput

# ======================
# FUZZY LOGIC DEFINITION
# ======================

# Input fuzzy sets (distance in mm)
input_sets = {
    "distance": {
        "close": gaussian(0, 200),
        "medium": gaussian(1500, 500),
        "far": gaussian(3000, 400)
    }
}

# Output fuzzy sets: Duty (0–100%)
duty_sets = {
    "low": trapezoidal(0, 0, 20, 40),
    "medium": triangular(30, 50, 70),
    "high": trapezoidal(60, 80, 100, 100)
}

# Output fuzzy sets: Frequency (100–2000 Hz)
freq_sets = {
    "low": gaussian(300, 150),
    "medium": gaussian(1000, 300),
    "high": gaussian(1700, 200)
}

# Combine outputs
output_sets = {
    "duty": duty_sets,
    "freq": freq_sets
}

# Output ranges
output_ranges = {
    "duty": (0, 100),
    "freq": (100, 2000)
}

# Rules (dynamic 4-rule system)
rules = [
    {"if": {"distance": "close"}, "then": {"freq": "high", "duty": "medium"}},
    {"if": {"distance": "medium"}, "then": {"freq": "medium", "duty": "high"}},
    {"if": {"distance": "far"}, "then": {"freq": "low", "duty": "low"}},
    {"if": {"distance": "close"}, "then": {"freq": "high", "duty": "high"}}
]

# Initialize fuzzy controller
fuzzy = FuzzyCore(input_sets, output_sets, rules, output_ranges)

# ======================
# HARDWARE SETUP
# ======================

# Ultrasonic sensor on pins 15 (trig) and 16 (echo)
ultra = Ultrasonic(trig_pin=15, echo_pin=16)

# Generic PWM output (buzzer or any PWM device) on pin 14
output_device = PWMOutput(pin=14, mode="buzzer")

# ======================
# MAIN LOOP
# ======================

while True:
    distance_mm = ultra.read()
    if distance_mm is None:
        output_device.off()
        time.sleep(0.1)
    
    print("Distance:", distance_mm, "mm")

    # Compute fuzzy outputs
    fuzzy_out = fuzzy.compute({"distance": distance_mm})
    
    duty_percent = fuzzy_out["duty"]
    freq_hz = fuzzy_out["freq"]

    # Clamp frequency to safe range
    freq_hz = min(max(100, freq_hz), 2000)

    # Update PWM output (continuous theremin mode)
    output_device.update(freq=freq_hz, duty=duty_percent)

    # Smooth update rate
    time.sleep(0.1)
