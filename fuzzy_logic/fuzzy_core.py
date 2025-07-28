class FuzzyCore:
    def __init__(self, input_sets, output_sets, rules, output_ranges):
        """
        input_sets: dict
            {"distance": {"close": fn, "medium": fn, ...}, "temp": {...}}
        output_sets: dict
            {"pwm": {"low": fn, "high": fn}, "servo": {"left": fn, ...}}
        rules: list of dict
            [
              {"if": {"distance": "close"}, "then": {"pwm": "high"}},
              {"if": {"temp": "hot"}, "then": {"servo": "left"}}
            ]
        output_ranges: dict
            {"pwm": (0, 100), "servo": (-45, 45)}  # crisp output ranges
        """
        self.input_sets = input_sets
        self.output_sets = output_sets
        self.rules = rules
        self.output_ranges = output_ranges

    # ---------- Fuzzification ----------
    def fuzzify(self, inputs):
        """
        inputs: {"distance": 120, "temp": 30}
        returns: {"distance": {"close": 0.2, ...}, "temp": {...}}
        """
        fuzzified = {}
        for var_name, value in inputs.items():
            if value is None:
                fuzzified[var_name] = {label: 0.0 for label in self.input_sets[var_name]}
                continue
            sets = self.input_sets[var_name]
            fuzzified[var_name] = {label: fn(value) for label, fn in sets.items()}
        return fuzzified

    # ---------- Apply Rules ----------
    def apply_rules(self, fuzzified):
        """
        Returns activations for each output variable's fuzzy sets
        Example: {"pwm": {"high": 0.7, "low": 0.2}, "servo": {"left": 0.5}}
        """
        # Initialize all outputs with 0 activation
        activations = {out: {label: 0.0 for label in sets}
                       for out, sets in self.output_sets.items()}

        # Evaluate each rule
        for rule in self.rules:
            # Rule conditions (min across multiple inputs)
            conditions = rule["if"]
            values = [fuzzified[var][label] for var, label in conditions.items()]
            rule_strength = min(values)

            # Apply to all outputs defined in "then"
            for out_var, out_label in rule["then"].items():
                activations[out_var][out_label] = max(
                    activations[out_var][out_label], rule_strength
                )

        return activations

    # ---------- Aggregate + Defuzzify ----------
    def aggregate_and_defuzzify(self, activations):
        """
        For each output variable:
          - Build aggregated membership across domain
          - Defuzzify via centroid
        Returns crisp outputs: {"pwm": value, "servo": value}
        """
        crisp_outputs = {}

        for out_var, sets in self.output_sets.items():
            out_min, out_max = self.output_ranges[out_var]
            step = 1 if out_var == 'duty' else 10
            domain = list(range(out_min, out_max + 1, step))

            aggregated = []
            for x in domain:
                # For each label in this output variable
                memberships = [
                    min(activations[out_var][label], fn(x))
                    for label, fn in sets.items()
                ]
                aggregated.append(max(memberships))

            # Defuzzify centroid
            numerator = sum(x * mu for x, mu in zip(domain, aggregated))
            denominator = sum(aggregated) or 1.0
            crisp_outputs[out_var] = numerator / denominator

        return crisp_outputs

    # ---------- Full Pipeline ----------
    def compute(self, inputs):
        fuzzified = self.fuzzify(inputs)
        activations = self.apply_rules(fuzzified)
        if all(all(val==0 for val in out.values()) for out in activations.values()):
            return {out_var: self.output_ranges[out_var][0] for out_var in self.output_sets}
        return self.aggregate_and_defuzzify(activations)
