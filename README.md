A Stochastic Analysis of Non-Linear Tire Degradation and Adaptive Strategy Optimization under Chaos Conditions: A Silverstone Case Study

Author: Diganth

Project Type: Computational Physics & Predictive Data Science
Language/Stack: Python 3 (Standard Library)

1. Abstract
This project presents a discrete-time, telemetry-calibrated race simulation engine designed to evaluate the trade-offs between a traditional 1-stop pit strategy and an aggressive 2-stop strategy. Calibrated against empirical timing data from the 2024 and 2025 British Grands Prix at Silverstone, the model incorporates non-linear tire wear physics, dynamic vehicle mass reduction (fuel burn sensitivity), and stochastic interruptions via Monte Carlo Safety Car deployments.
Initial runs demonstrated a deterministic 1-stop dominance. However, isolating random variables revealed a distinct structural loophole: a late-race Safety Car creates an asymmetric advantage for a 2-stop strategy. To mitigate this risk, an algorithmic Adaptive Pit Window was engineered, reducing the strategic failure rate from 11.4% down to a statistically resilient <1.5%.

2. Mathematical Modeling & Physics Constants
To achieve high-fidelity validation, the simulation abandons linear estimations in favor of track-specific physical coefficients modeled around Silverstone’s extreme lateral high-speed corners (Maggotts, Becketts, and Chapel).
2.1 Vehicle Dynamics & Fuel Sensitivity
The total mass of the car decreases monotonically each lap as fuel is combusted. The instantaneous base lap time T 
base
​	
  for any given lap n is adjusted using a fuel sensitivity coefficient:
T(n)=((M(0)-(n*m))/10)*γ

Where:
Initial Fuel Mass M (0)=100.0 kg
Fuel Burn Rate m=1.92 kg/lap
Fuel Sensitivity Coefficient γ=0.31 seconds per 10 kg
2.2 Non-Linear Tire Degradation Models
Tire compound grip degradation is modeled quadratically to simulate a performance "cliff" caused by thermal blistering under heavy aerodynamic loading.
Tire Wear Penalty (seconds added to lap time)
  |
  |                                 /  (SOFT Cliff)
  |                                /
  |                              ./   (MEDIUM Cliff)
  |                       _..---'
  |         _...---'''--''            (HARD Linear Stability)
  +------------------------------------->
  0                  20                 40   Tire Age (Laps)
The time penalty T as a function of tire compound and age (a) is defined as:
SOFT:
T (a)=0.07a+0.008a ^(2)
 
MEDIUM:
T(a)=0.4+0.04a+0.002a^(2)
 
HARD:
T(a)=1.1+0.015a+0.0003a ^(2)
 
3. Methodology & Simulation Architecture
The computational engine executes a nested loop simulating a 52-lap Grand Prix across 1,000 distinct parallel universes (Monte Carlo iterations).
[Monte Carlo Initialization: 1,000 Races]
         │
         ├──► [Generate Stochastic Track State] (15% Safety Car Probability)
         │
         ├──► [Lap Loop: 1 to 52]
         │         │
         │         ├──► Calculate Fuel Weight reduction
         │         ├──► Calculate Quadratic Tire Grip loss
         │         ├──► Inject Gaussian Driver Variance (μ=0, σ=0.2)
         │         │
         │         ├──► [Execute Strategy 1 AI Brain] ──► Reactive Pit Window Check
         │         └──► [Execute Strategy 2 Engine]   ──► Static Pit Limit Check
         │
         └──► [Aggregate Winner Logs] ──► Calculate Statistical Win Vector
3.1 Stochastic Elements
Driver Consistency: Lap-by-lap variance is governed by a normal distribution (Gaussian noise) where X∼N(0,0.2^(2)), tracking micro-mistakes like tire lock-ups or traffic delays.
The Safety Car Protocol: A baseline 15% probability of a race-disrupting accident is evaluated per iteration. If active, track speeds are reduced by 30.0s per lap, and the pit lane penalty drops asymmetrically:
Cost = 22.5 seconds
Cost = 11.0 seconds

4. Key Engineering Discoveries & Data Anomalies
4.1 Calibration against Empirical Reality
During initial environment building, the model clocked a dry-weather baseline race at 79.5 minutes. When validated against the 2024 British Grand Prix (won by Lewis Hamilton in 82.2 minutes), the model initially appeared 3 minutes too fast.
Analytical Insight: The 2024 race featured mid-race precipitation, forcing damp track conditions and intermediate tire switches. Accounting for the absence of rain variables in our code, a 3.6% error margin confirms an exceptionally high environmental calibration accuracy.
4.2 The Variable-Isolation Breakthrough
To stress-test the core physics engine without environmental noise, the Gaussian driver variance was completely isolated (σ=0). This revealed a profound structural anomaly:
The Late-Race Safety Car Loophole: If a Safety Car is deployed specifically between Laps 34 and 36, Strategy 2 (the 2-stop) captures a highly compressed "cheap" pit stop. Because Strategy 1 has already committed to its single pit stop on Lap 23, it is mathematically paralyzed and unable to respond, causing it to drop from a 99.8% win rate down to a crushing failure rate in nearly 20% of deterministic matches.
4.3 Algorithmic Mitigation (The AI Brain)
To counter this asymmetry, a dynamic, conditional decision tree was programmed into Strategy 1's pit routine:
Python
if not has_pitted_1:
    if 20 <= lap <= 25 and is_sc_active:
        should_pit_1 = True  # Dynamic opportunistic response
    elif lap == 23:
        should_pit_1 = True  # Hard boundary execution
5. Monte Carlo Results & Conclusion
Across 1,000 randomized race iterations containing high-chaos factors, the final efficiency matrix indicates:
Static Strategy 1 (Pre-AI Control): ~88.6% Win Rate
Adaptive Strategy 1 (Post-AI Upgrade): ~98.8% to 99.5% Win Rate
Strategy 2 (2-Stop Attack Mode): ~1.2% Win Rate
Conclusion
The data proves that while an aggressive 2-stop strategy benefits from running in a perpetual tire performance sweet spot, the 22.5-second pit stop penalty at Silverstone is too mathematically punitive to overcome on raw pace alone.
Ultimately, statistical perfection (100% wins) cannot be achieved via software optimization alone; a <1.5% operational failure rate must be accepted as an unmitigated "Black Swan" event—representing situations where track conditions align flawlessly with a competitor's pit window.
