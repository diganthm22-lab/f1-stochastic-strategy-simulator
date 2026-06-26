# A Stochastic Analysis of Non-Linear Tire Degradation and Weather-Adaptive Strategy Optimization under Chaos Conditions

**Author:** Diganth Maruthi

**Project Type:** Computational Physics, Predictive Data Science & Interactive Simulation  
**Language/Stack:** Python 3 (Standard Library)  

---

## 1. Abstract
This project presents an interactive, discrete-time race simulation engine designed to evaluate custom user-defined pit strategies against an AI-optimized baseline. Calibrated using empirical parameters from the British Grand Prix at Silverstone, the model evaluates how a chosen strategy holds up when subjected to multi-layered stochastic interruptions: a 15% probability of a Safety Car and an independent 7% chance of mid-race precipitation. 

The core architecture forces reactive decision-making: if rain falls, the simulation overrides deterministic models, forcing vehicles to pivot to wet-weather compounds. This framework serves as a tool for studying risk mitigation and real-time optimization in high-stakes environments.

---

## 2. Mathematical Modeling & Track Physics

The simulation abandons linear wear approximations in favor of track-specific physical coefficients modeled around Silverstone’s high-speed, high-lateral-load characteristics.

### 2.1 Vehicle Dynamics & Fuel Mass Sensitivity
The total mass of the car decreases monotonically each lap as fuel is combusted. The instantaneous base lap time $T_{\text{base}}$ for any given lap $n$ is adjusted using a fuel sensitivity coefficient:

$$T_{\text{fuel}}(n) = \left( \frac{M_{\text{fuel}}(0) - (n \times \dot{m})}{10} \right) \times \gamma$$

**Parameters:**
* Initial Fuel Mass $M_{\text{fuel}}(0) = 100.0 \text{ kg}$
* Fuel Burn Rate $\dot{m} = 1.92 \text{ kg/lap}$
* Fuel Sensitivity Coefficient $\gamma = 0.31 \text{ seconds per 10 kg}$

### 2.2 Non-Linear Tire Degradation Models
Slick tire compounds lose grip quadratically to simulate thermal degradation and blistering. A specialized wet-weather compound (**Intermediate**) is included, which maintains structural stability in rain but suffers an efficiency penalty under dry track conditions.

The time penalty $T_{\text{wear}}$ as a function of tire compound and age ($a$) is defined as:

* **SOFT:** $T_{\text{soft}}(a) = 0.07a + 0.008a^2$
* **MEDIUM:** $T_{\text{medium}}(a) = 0.4 + 0.04a + 0.002a^2$
* **HARD:** $T_{\text{hard}}(a) = 1.1 + 0.015a + 0.0003a^2$
* **INTERMEDIATE:** $T_{\text{inter}}(a) = 1.5 + 0.02a$

---

## 3. Architecture & Multi-Variable Chaos Logic

The engine executes a nested loop simulating a 52-lap Grand Prix across 1,000 distinct parallel universes (Monte Carlo iterations).re track conditions align flawlessly with a competitor's pit window.

### 3.1 Environmental Disruption Protocols
1. **Gaussian Noise:** Micro-variances in driver consistency (lock-ups, traffic) are introduced on every lap via normal distribution noise where $X \sim \mathcal{N}(0, 0.2^2)$.
2. **Asymmetric Pit Lane Costs:** Under normal conditions, a pit stop costs 22.5s. If a Safety Car is deployed, field normalization drops the effective pit penalty to 11.0s.
3. **Dynamic Weather Shift:** If the 7% rain threshold is met, slick tires immediately incur a massive **+15.0s penalty per lap** due to hydroplaning risks, forcing an immediate, reactive pit stop for Intermediate tires.

---

## 4. Key Engineering Discoveries & Edge Cases

### 4.1 Weather-Induced Strategy Inversion
When evaluating a standard dry race, a Medium $\rightarrow$ Hard 1-stop strategy dominates with a near-perfect win rate against a 2-stop configuration. However, introducing the 7% rain mechanic alters the model's structural hierarchy. 

If rain occurs *before* a car's scheduled pit window, the "sunk cost" of a planned stop is eliminated. Both cars are forced to improvise. The winner of these chaotic iterations is almost always determined by who was closest to the pit entry when the weather state flipped—simulating the real-world high-variance nature of motorsport strategy.

---

## 5. How to Run the Interactive Simulation

The project features an interactive Command Line Interface (CLI). To run the Monte Carlo predictive tool:

1. Clone the repository and execute the script:
```bash
python simulator.py
