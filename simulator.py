import random

def calculate_silverstone_tire_wear(compound, tire_age):
    if compound == "SOFT":
        return (tire_age * 0.07) + (tire_age ** 2) * 0.008
    elif compound == "MEDIUM":
        return 0.4 + (tire_age * 0.04) + (tire_age ** 2) * 0.002
    elif compound == "HARD":
        return 1.1 + (tire_age * 0.015) + (tire_age ** 2) * 0.0003

# Track Constants
TOTAL_LAPS = 52
NORMAL_PIT_PENALTY = 22.5
SAFETY_CAR_PIT_PENALTY = 11.0
FUEL_BURN_PER_LAP = 1.92
FUEL_EFFECT_PER_10KG = 0.31
BASE_LAP_TIME = 87.0

strat_1_wins = 0
strat_2_wins = 0
total_simulations = 1000

print(f"🧠 Running {total_simulations} simulations with AI Adaptive Strategy...")

for race in range(1, total_simulations + 1):
    
    # 15% chance a crash happens, randomly picking a lap between 10 and 40
    has_safety_car = random.random() < 0.15
    safety_car_lap = random.randint(10, 40) if has_safety_car else -1

    # Reset Car 1 (AI Adaptive)
    time_1stop = 0.0
    compound_1stop = "MEDIUM"
    age_1stop = 0
    fuel_1stop = 100.0
    has_pitted_1 = False  # Track if Car 1 already made its stop

    # Reset Car 2 (Fixed 2-Stop)
    time_2stop = 0.0
    compound_2stop = "SOFT"
    age_2stop = 0
    fuel_2stop = 100.0

    for lap in range(1, TOTAL_LAPS + 1):
        is_sc_active = (lap == safety_car_lap)

        # --- CAR 1: AI ADAPTIVE PIT WINDOW LOGIC ---
        should_pit_1 = False
        
        if not has_pitted_1:
            # Condition A: We hit a Safety Car during our flexible window (Laps 20 to 25) -> DIVINE INTERVENTION! PIT NOW!
            if 20 <= lap <= 25 and is_sc_active:
                should_pit_1 = True
            # Condition B: We reached the absolute limit of our window (Lap 23) and no Safety Car happened.
            elif lap == 23:
                should_pit_1 = True

        if should_pit_1:
            pit_cost = SAFETY_CAR_PIT_PENALTY if is_sc_active else NORMAL_PIT_PENALTY
            time_1stop += pit_cost
            compound_1stop = "HARD"
            age_1stop = 0
            has_pitted_1 = True
            
        fuel_penalty_1 = (fuel_1stop / 10.0) * FUEL_EFFECT_PER_10KG
        tire_penalty_1 = calculate_silverstone_tire_wear(compound_1stop, age_1stop)
        lap_time_1 = BASE_LAP_TIME + fuel_penalty_1 + tire_penalty_1 + random.normalvariate(0, 0.2)
        if is_sc_active: lap_time_1 += 30.0
        time_1stop += lap_time_1
        fuel_1stop -= FUEL_BURN_PER_LAP
        age_1stop += 1

        # --- CAR 2: FIXED STRATEGY LOGIC ---
        if lap == 15 or lap == 35:
            pit_cost = SAFETY_CAR_PIT_PENALTY if is_sc_active else NORMAL_PIT_PENALTY
            time_2stop += pit_cost
            compound_2stop = "MEDIUM"
            age_2stop = 0
            
        fuel_penalty_2 = (fuel_2stop / 10.0) * FUEL_EFFECT_PER_10KG
        tire_penalty_2 = calculate_silverstone_tire_wear(compound_2stop, age_2stop)
        lap_time_2 = BASE_LAP_TIME + fuel_penalty_2 + tire_penalty_2 + random.normalvariate(0, 0.2)
        if is_sc_active: lap_time_2 += 30.0
        time_2stop += lap_time_2
        fuel_2stop -= FUEL_BURN_PER_LAP
        age_2stop += 1

    if time_1stop < time_2stop:
        strat_1_wins += 1
    else:
        strat_2_wins += 1

print("\n=========================================================")
print("📊 FINAL TELEMETRY: AI BRAIN VS FIXED STRATEGY")
print("=========================================================")
print(f"Strategy 1 (AI 1-Stop: M -> H) Wins: {strat_1_wins} races ({round((strat_1_wins/total_simulations)*100, 1)}%)")
print(f"Strategy 2 (Fixed 2-Stop)     Wins: {strat_2_wins} races ({round((strat_2_wins/total_simulations)*100, 1)}%)")
print("=========================================================")
