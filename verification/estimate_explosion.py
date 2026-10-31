"""Environment-only estimate with analytic truncation and Hoeffding bounds.

This script specialises the proved conversion model to b=c=1, d=2,
division rate 3, complete inhibitor export, and initial S=3, I=0.
It does not simulate the potentially explosive physical-time process.
"""

import json
import math
from pathlib import Path

import numpy as np


def estimate(n=200_000, horizon=10.0, seed=20261028, alpha=0.05):
    rng = np.random.default_rng(seed)
    clock = np.zeros(n)
    inhibitors = np.zeros(n, dtype=np.int64)
    prob_zero = np.ones(n)
    prob_one = np.zeros(n)
    active = np.arange(n)
    conversion_events = 0
    all_events = 0
    iterations = 0
    max_inhibitors = 0

    while active.size:
        iterations += 1
        counts = inhibitors[active]
        rates = 4.0 + 2.0 * counts
        next_times = clock[active] + rng.exponential(1.0 / rates)
        inside = next_times <= horizon
        event_ids = active[inside]
        if not event_ids.size:
            break
        event_times = next_times[inside]
        event_rates = rates[inside]
        event_counts = counts[inside]
        clock[event_ids] = event_times
        marks = rng.random(event_ids.size) * event_rates
        immigration = marks < 1.0
        conversion = (marks >= 1.0) & (marks < 1.0 + 2.0 * event_counts)
        catastrophe = ~(immigration | conversion)

        inhibitors[event_ids[immigration | conversion]] += 1
        inhibitors[event_ids[catastrophe]] = 0
        loss_ids = event_ids[conversion]
        if loss_ids.size:
            q = np.exp(-event_times[conversion])
            old_zero = prob_zero[loss_ids].copy()
            prob_one[loss_ids] = prob_one[loss_ids] * (1.0 - q) + old_zero * q
            prob_zero[loss_ids] = old_zero * (1.0 - q)
        conversion_events += int(loss_ids.size)
        all_events += int(event_ids.size)
        max_inhibitors = max(max_inhibitors, int(inhibitors[event_ids].max()))
        active = event_ids

    sample = prob_zero + prob_one
    estimate_value = float(sample.mean())
    tail_bias = 2.0 * math.exp(-horizon) - math.exp(-2.0 * horizon)
    sampling_radius = math.sqrt(math.log(2.0 / alpha) / (2.0 * n))
    return {
        "model": {"b": 1, "c": 1, "d": 2, "lambda": 3, "p": 0,
                  "initial_s": 3, "initial_i": 0},
        "samples": n,
        "operational_horizon": horizon,
        "seed": seed,
        "numpy_version": np.__version__,
        "estimator": "Poisson-binomial P(K_U < 2), conditional on inhibitor environment",
        "sample_mean": estimate_value,
        "sample_sd": float(sample.std(ddof=1)),
        "deterministic_upper_bound_on_truncation_bias": tail_bias,
        "confidence_level": 1.0 - alpha,
        "hoeffding_sampling_radius": sampling_radius,
        "confidence_interval_for_true_explosion_probability": [
            max(0.0, estimate_value - sampling_radius - tail_bias),
            min(1.0, estimate_value + sampling_radius),
        ],
        "analytical_lower_bound": "1/2",
        "simulated_environment_events": all_events,
        "simulated_conversion_events": conversion_events,
        "max_event_iterations_for_any_sample": iterations,
        "max_observed_inhibitor_count": max_inhibitors,
        "claim_limit": "The interval combines a proved truncation bound with a Hoeffding sampling bound; numerical random generation and floating-point arithmetic are not formally verified.",
    }


if __name__ == "__main__":
    result = estimate()
    target = Path(__file__).with_name("explosion_estimate.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
