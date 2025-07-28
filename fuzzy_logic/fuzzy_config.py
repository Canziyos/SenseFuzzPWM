from membership import gaussian, trapezoidal, triangular

# ======================
# Fuzzy logic definition
# ======================

# Input fuzzy sets (distance in mm) + motion (binary)
input_sets = {
    "distance": {
        "close": gaussian(0, 200),
        "medium": gaussian(1500, 500),
        "far": gaussian(3000, 400)
    },
    "motion": {
        "no_motion": lambda x: 1.0 if x == 0 else 0.0,
        "motion": lambda x: 1.0 if x == 1 else 0.0
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

# Rules (currently motion only; distance rules commented for now)
rules = [
    # Motion-based rules
    {"if": {"motion": "motion"}, "then": {"freq": "high", "duty": "high"}},
    {"if": {"motion": "no_motion"}, "then": {"freq": "low", "duty": "low"}},

    # Distance-based rules (can re-enable later)
    # {"if": {"distance": "close"}, "then": {"freq": "high", "duty": "medium"}},
    # {"if": {"distance": "medium"}, "then": {"freq": "medium", "duty": "high"}},
    # {"if": {"distance": "far"}, "then": {"freq": "low", "duty": "low"}},
    # {"if": {"distance": "close"}, "then": {"freq": "high", "duty": "high"}}
]
