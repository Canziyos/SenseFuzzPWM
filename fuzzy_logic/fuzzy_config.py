from membership import gaussian, trapezoidal, triangular

# ======================
# Fuzzy logic definition
# ======================

# Input fuzzy sets (distance in mm)
input_sets = {
    "distance": {
        "very_close": gaussian(500, 300),   # 0–600 mm range
        "close": gaussian(1000, 300),        # overlaps with very_close & medium
        "medium": gaussian(1500, 300),      # central zone
        "far": gaussian(2000, 300)          # overlaps with medium
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

# Rules using 4 distance memberships
rules = [
    {"if": {"distance": "very_close"}, "then": {"freq": "high", "duty": "high"}},
    {"if": {"distance": "close"},      "then": {"freq": "high", "duty": "medium"}},
    {"if": {"distance": "medium"},     "then": {"freq": "medium", "duty": "low"}},
    {"if": {"distance": "far"},        "then": {"freq": "low", "duty": "low"}}
]
