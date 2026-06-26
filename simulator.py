import random

def calculate_silverstone_tire_wear(compound, tire_age):
    if compound == "SOFT":
        return (tire_age * 0.07) + (tire_age ** 2) * 0.008
    elif compound == "MEDIUM":
        return 0.4 + (tire_age * 0.04) + (tire_age ** 2) * 0.002
    elif compound == "HARD":
        return 1.1 + (tire_age * 0.015) + (tire_age ** 2) * 0.0003
    elif compound == "INTERMEDIATE":
        # Great in rain (+0.0s penalty), but slows down massively if track is dry
        return 1.5 + (tire_age * 0.02)

# Track Constants
TOTAL_LAPS = 52
NORMAL_PIT_PENALTY = 22.5
SAFETY_CAR_PIT_PENALTY = 11.0
FUEL_BURN_PER_LAP = 1.92
FUEL_EFFECT_PER_10KG = 0.31
BASE_LAP_TIME = 87.0

print("=========================================================")
print("LIVE SILVERSTONE STRATEGY DESK️")
print("=========================================================")

# Get interactive inputs from the user
user_start_tire = input("Choose Car 1 Starting Tire (SOFT/MEDIUM/HARD): ").upper().strip()
user_pit_lap = int(input("Choose Car 1 Planned Pit Stop Lap (e.g., 23): "))
user_target_tire = input("Choose Car 1 Target Pit Tire (SOFT/MEDIUM/HARD): ").upper().strip()

print("\n=========================================================")
print("Running 1,000 simulations...")
print("=========================================================")

strat_1_wins = 0
strat_2_wins = 0
rain_races_count = 0

for race in range(1, 1001):
    
    # 15% Safety Car risk
    has_safety_car = random.random() < 0.15
    safety_car_lap = random.randint(10, 40) if has_safety_car else -1

    # 7% Rain risk per race
    will_it_rain = random.random() < 0.07
    rain_start_lap = random.randint(15, 35) if will_it_rain else -1
    if will_it_rain:
        rain_races_count += 1

    # Reset Car 1 (User Customizable Strategy)
    time_1stop = 0.0
    compound_1stop = user_start_tire
    age_1stop = 0
    fuel_1stop = 100.0
    has_pitted_1 = False

    # Reset Car 2 (The AI Benchmark Strategy)
    time_2stop = 0.0
    compound_2stop = "MEDIUM"
    age_2stop = 0
    fuel_2stop = 100.0
    has_pitted_2 = False

    for lap in range(1, TOTAL_LAPS + 1):
        is_sc_active = (lap == safety_car_lap)
        is_raining = (will_it_rain and lap >= rain_start_lap)

        # --- CAR 1 LOGIC (User Settings + Emergency Rain Response) ---
        should_pit_1 = False
        
        if is_raining and compound_1stop != "INTERMEDIATE":
            should_pit_1 = True  # Emergency rain switch!
            next_compound_1 = "INTERMEDIATE"
        elif not has_pitted_1 and lap == user_pit_lap:
            should_pit_1 = True  # Planned user pit stop
            next_compound_1 = user_target_tire

        if should_pit_1:
            pit_cost = SAFETY_CAR_PIT_PENALTY if is_sc_active else NORMAL_PIT_PENALTY
            time_1stop += pit_cost
            compound_1stop = next_compound_1
            age_1stop = 0
            if not is_raining:  # Only count as planned stop if it didn't rain
                has_pitted_1 = True
            
        fuel_penalty_1 = (fuel_1stop / 10.0) * FUEL_EFFECT_PER_10KG
        tire_penalty_1 = calculate_silverstone_tire_wear(compound_1stop, age_1stop)
        
        # Rain penalty if slick tires are left on wet asphalt
        if is_raining and compound_1stop != "INTERMEDIATE":
            tire_penalty_1 += 15.0  # Massive driving penalty on wrong tires
            
        lap_time_1 = BASE_LAP_TIME + fuel_penalty_1 + tire_penalty_1 + random.normalvariate(0, 0.2)
        if is_sc_active: lap_time_1 += 30.0
        time_1stop += lap_time_1
        fuel_1stop -= FUEL_BURN_PER_LAP
        age_1stop += 1

        # --- CAR 2 LOGIC (AI Benchmark + Rain Response) ---
        should_pit_2 = False
        if is_raining and compound_2stop != "INTERMEDIATE":
            should_pit_2 = True
            next_compound_2 = "INTERMEDIATE"
        elif not has_pitted_2 and lap == 23:
            should_pit_2 = True
            next_compound_2 = "HARD"

        if should_pit_2:
            pit_cost = SAFETY_CAR_PIT_PENALTY if is_sc_active else NORMAL_PIT_PENALTY
            time_2stop += pit_cost
            compound_2stop = next_compound_2
            age_2stop = 0
            if not is_raining:
                has_pitted_2 = True
            
        fuel_penalty_2 = (fuel_2stop / 10.0) * FUEL_EFFECT_PER_10KG
        tire_penalty_2 = calculate_silverstone_tire_wear(compound_2stop, age_2stop)
        
        if is_raining and compound_2stop != "INTERMEDIATE":
            tire_penalty_2 += 15.0
            
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
print("FINAL STRATEGY EXECUTIONS REPORT")
print("=========================================================")
print(f"Total Weather Anomalies (Rain): {rain_races_count} out of 1000 races")
print(f"Your Custom Strategy Wins: {strat_1_wins} ({round((strat_1_wins/1000)*100, 1)}%)")
print(f"AI Strategy Wins: {strat_2_wins} ({round((strat_2_wins/1000)*100, 1)}%)")
print("=========================================================")
