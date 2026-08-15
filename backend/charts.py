import pandas as pd
import matplotlib.pyplot as plt


# =========================
# GRAPH 1
# MUSCLE GROUP FREQUENCY
# =========================

def showMuscleGroupFrequency(data):
    df = pd.DataFrame(
        data,
        columns=["muscle_group", "frequency"]
    )

    if df.empty:
        print("No muscle group data available.")
        return

    plt.figure()

    plt.bar(
        df["muscle_group"],
        df["frequency"]
    )

    # Goal line
    plt.axhline(
        y=2,
        linestyle="--",
        label="Goal: 2x per week"
    )

    # Horizontal grid lines
    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.xlabel("Muscle Group")
    plt.ylabel("Workouts Per Week")
    plt.title("Weekly Muscle Group Frequency")

    plt.legend()
    plt.tight_layout()
    plt.show()


# =========================
# GRAPH 2
# PROGRESSIVE OVERLOAD
# =========================

def showProgressiveOverload(data, exercise_name):
    df = pd.DataFrame(
        data,
        columns=[
            "workout_date",
            "weight",
            "reps"
        ]
    )

    if df.empty:
        print("No workout data available.")
        return

    df["workout_date"] = pd.to_datetime(
        df["workout_date"]
    )

    df = df.sort_values(
        "workout_date"
    )

    # Find the heaviest weight used each workout
    progression = (
        df.groupby("workout_date")["weight"]
        .max()
        .reset_index()
    )

    plt.figure()

    plt.plot(
        progression["workout_date"],
        progression["weight"],
        marker="o"
    )

    plt.xlabel("Workout Date")
    plt.ylabel("Highest Weight (lb)")
    plt.title(
        f"{exercise_name} Progressive Overload"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# =========================
# GRAPH 3
# ESTIMATED ONE REP MAX
# =========================

def showEstimatedOneRepMax(data, exercise_name):
    df = pd.DataFrame(
        data,
        columns=[
            "workout_date",
            "weight",
            "reps"
        ]
    )

    if df.empty:
        print("No workout data available.")
        return

    df["workout_date"] = pd.to_datetime(
        df["workout_date"]
    )

    # Epley formula
    df["estimated_1rm"] = (
        df["weight"]
        * (1 + df["reps"] / 30)
    )

    # Best estimated 1RM from each workout
    progression = (
        df.groupby("workout_date")["estimated_1rm"]
        .max()
        .reset_index()
    )

    progression = progression.sort_values(
        "workout_date"
    )

    plt.figure()

    plt.plot(
        progression["workout_date"],
        progression["estimated_1rm"],
        marker="o"
    )

    plt.xlabel("Workout Date")
    plt.ylabel("Estimated 1RM (lb)")
    plt.title(
        f"{exercise_name} Estimated 1RM Progress"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# =========================
# GRAPH 4
# WHAT-IF PROJECTION
# =========================

def showWhatIfProjection(
    starting_weight,
    increase_amount,
    number_of_periods,
    exercise_name
):
    periods = list(
        range(number_of_periods + 1)
    )

    projected_weights = []

    current_weight = starting_weight

    for period in periods:
        projected_weights.append(
            current_weight
        )

        current_weight += increase_amount

    df = pd.DataFrame({
        "period": periods,
        "projected_weight": projected_weights
    })

    plt.figure()

    plt.plot(
        df["period"],
        df["projected_weight"],
        marker="o"
    )

    plt.xlabel("Progression Period")
    plt.ylabel("Projected Weight (lb)")
    plt.title(
        f"{exercise_name} What-If Projection"
    )

    plt.tight_layout()
    plt.show()

def showExerciseStatistics(data, exercise_name):
    df = pd.DataFrame(
        data,
        columns=[
            "workout_date",
            "weight",
            "reps"
        ]
    )

    if df.empty:
        print("No workout data available.")
        return

    # -------------------------
    # BASIC WEIGHT STATISTICS
    # -------------------------

    mean_weight = df["weight"].mean()
    median_weight = df["weight"].median()
    minimum_weight = df["weight"].min()
    maximum_weight = df["weight"].max()

    weight_range = (
        maximum_weight - minimum_weight
    )

    standard_deviation = df["weight"].std()


    # -------------------------
    # REP STATISTICS
    # -------------------------

    average_reps = df["reps"].mean()


    # -------------------------
    # VOLUME
    # -------------------------

    df["volume"] = (
        df["weight"] * df["reps"]
    )

    average_set_volume = df["volume"].mean()
    total_volume = df["volume"].sum()


    # -------------------------
    # ESTIMATED 1RM
    # -------------------------

    def calculate1RM(row):

        if row["reps"] == 1:
            return row["weight"]

        return (
            row["weight"]
            * (1 + row["reps"] / 30)
        )


    df["estimated_1rm"] = df.apply(
        calculate1RM,
        axis=1
    )

    best_estimated_1rm = (
        df["estimated_1rm"].max()
    )


    # -------------------------
    # TOTALS
    # -------------------------

    total_sets = len(df)

    total_workouts = (
        df["workout_date"]
        .nunique()
    )


    # -------------------------
    # DISPLAY
    # -------------------------

    print(
        f"\n--- {exercise_name} Statistics ---"
    )

    print(f"Total Workouts: {total_workouts}")
    print(f"Total Sets: {total_sets}")

    print("\n--- Weight ---")
    print(f"Mean Weight: {mean_weight:.1f} lb")
    print(f"Median Weight: {median_weight:.1f} lb")
    print(f"Minimum Weight: {minimum_weight:.1f} lb")
    print(f"Maximum Weight: {maximum_weight:.1f} lb")
    print(f"Weight Range: {weight_range:.1f} lb")

    if pd.notna(standard_deviation):
        print(
            f"Standard Deviation: "
            f"{standard_deviation:.1f} lb"
        )
    else:
        print("Standard Deviation: N/A")

    print("\n--- Reps ---")
    print(f"Average Reps: {average_reps:.1f}")

    print("\n--- Volume ---")
    print(
        f"Average Set Volume: "
        f"{average_set_volume:.1f} lb"
    )

    print(
        f"Total Volume: "
        f"{total_volume:.1f} lb"
    )

    print("\n--- Strength ---")
    print(
        f"Best Estimated 1RM: "
        f"{best_estimated_1rm:.1f} lb"
    )