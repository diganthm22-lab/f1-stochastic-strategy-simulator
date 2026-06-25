# A Stochastic Analysis of Non-Linear Tire Degradation and Adaptive Strategy Optimization under Chaos Conditions: A Silverstone Case Study

**Author:** Diganth 
**Project Type:** Computational Physics & Predictive Data Science  
**Language/Stack:** Python 3 (Standard Library)  

---

## 1. Abstract
This project presents a discrete-time, telemetry-calibrated race simulation engine designed to evaluate the trade-offs between a traditional 1-stop pit strategy and an aggressive 2-stop strategy. Calibrated against empirical timing data from the 2024 and 2025 British Grands Prix at Silverstone, the model incorporates non-linear tire wear physics, dynamic vehicle mass reduction (fuel burn sensitivity), and stochastic interruptions via Monte Carlo Safety Car deployments. 

Initial runs demonstrated a deterministic 1-stop dominance. However, isolating random variables revealed a distinct structural loophole: a late-race Safety Car creates an asymmetric advantage for a 2-stop strategy. To mitigate this risk, an algorithmic Adaptive Pit Window was engineered, reducing the strategic failure rate from 11.4% down to a statistically resilient <1.5%.

---

## 2. Mathematical Modeling & Physics Constants

To achieve high-fidelity validation, the simulation abandons linear estimations in favor of track-specific physical coefficients modeled around Silverstone’s extreme lateral high-speed corners (Maggotts, Becketts, and Chapel).

### 2.1 Vehicle Dynamics & Fuel Sensitivity
The total mass of the car decreases monotonically each lap as fuel is combusted. The instantaneous base lap time $T_{\text{base}}$ for any given lap $n$ is adjusted using a fuel sensitivity coefficient:

$$T_{\text{fuel}}(n) = \left( \frac{M_{\text{fuel}}(0) - (n \times \dot{m})}{10} \right) \times \gamma$$

**Parameters:**
* Initial Fuel Mass $M_{\text{fuel}}(0) = 100.0 \text{ kg}$
* Fuel Burn Rate $\dot{m} = 1.92 \text{ kg/lap}$
* Fuel Sensitivity Coefficient $\dots$ $\gamma = 0.31 \text{ seconds per 10 kg}$

### 2.2 Non-Linear Tire Degradation Models
Tire compound grip degradation is modeled quadratically to simulate a performance "cliff" caused by thermal blistering under heavy aerodynamic loading.

The time penalty $T_{\text{wear}}$ as a function of tire compound and age ($a$) is defined as:

* **SOFT:** $T_{\text{soft}}(a) = 0.07a + 0.008a^2$
* **MEDIUM:** $T_{\text{medium}}(a) = 0.4 + 0.04a + 0.002a^2$
* **HARD:** $T_{\text{hard}}(a) = 1.1 + 0.015a + 0.0003a^2$

---

## 3. Methodology & Simulation Architecture

The computational engine executes a nested loop simulating a 52-lap Grand Prix across 1,000 distinct parallel universes (Monte Carlo iterations).
