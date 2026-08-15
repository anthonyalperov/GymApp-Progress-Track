from database import (
    create_database,

    addUser,
    deleteUser,
    showAccountDetails,
    getUserId,
    checkLoginCredentials,

    addExercise,
    getUserExercises,
    deleteExercise,

    addWorkout,
    getUserWorkouts,
    deleteWorkout,
    displayRecentWorkout,

    addWorkoutSet,
    getWorkoutSets,
    deleteWorkoutSet
)


# =========================
# USER INPUT
# =========================

def getName() -> str:
    while True:
        name = input("Enter your Name: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def getAge() -> int:
    while True:
        try:
            age = int(input("Enter your Age: "))

            if age <= 0:
                print("Age must be greater than 0.")
                continue

            return age

        except ValueError:
            print("Please enter a valid number.")


def getBodyweight() -> float:
    while True:
        try:
            bodyweight = float(
                input("Enter your Body Weight in Lbs: ")
            )

            if bodyweight <= 0:
                print("Body weight must be greater than 0.")
                continue

            return bodyweight

        except ValueError:
            print("Please enter a valid number.")


def getUsername() -> str:
    while True:
        username = input("Enter your Username: ").strip()

        if username:
            return username

        print("Username cannot be empty.")


def getPassword() -> str:
    while True:
        password = input("Enter your Password: ").strip()

        if password:
            return password

        print("Password cannot be empty.")


# =========================
# USER ACCOUNT
# =========================

def createUser():
    while True:
        name = getName()
        age = getAge()
        bodyweight = getBodyweight()
        username = getUsername()
        password = getPassword()

        if addUser(
            name,
            age,
            bodyweight,
            username,
            password
        ):
            print("Account created successfully!")
            return

        print("That username already exists. Please try again.")


def displayAccountDetails(username, password):
    user = showAccountDetails(username, password)

    if not user:
        print("Account not found.")
        return

    print("\n--- Account Details ---")
    print(f"User ID: {user[0]}")
    print(f"Name: {user[1]}")
    print(f"Age: {user[2]}")
    print(f"Body Weight: {user[3]} lb")
    print(f"Username: {user[4]}")


# =========================
# EXERCISES
# =========================

def getExerciseInput(user_id):
    exercise_name = input(
        "Enter the exercise name: "
    ).strip()

    muscle_groups = {
        "1": "Chest",
        "2": "Back",
        "3": "Legs",
        "4": "Arms",
        "5": "Shoulders",
        "6": "Abs"
    }

    while True:
        print("\n--- Muscle Groups ---")

        for key, value in muscle_groups.items():
            print(f"{key}. {value}")

        choice = input(
            "Choose a muscle group: "
        ).strip()

        if choice in muscle_groups:
            muscle_group = muscle_groups[choice]
            break

        print("Invalid muscle group.")

    if addExercise(
        user_id,
        exercise_name,
        muscle_group
    ):
        print(f"{exercise_name} added successfully!")

    else:
        print(
            f"{exercise_name} already exists "
            "on your account."
        )


def chooseExercise(user_id):
    exercises = getUserExercises(user_id)

    if not exercises:
        print("You have no exercises available.")
        return None

    print("\n--- Your Exercises ---")

    for number, exercise in enumerate(
        exercises,
        start=1
    ):
        exercise_name = exercise[1]
        muscle_group = exercise[2]

        print(
            f"{number}. "
            f"{exercise_name} "
            f"({muscle_group})"
        )

    while True:
        try:
            choice = int(
                input("Choose an exercise: ")
            )

            if 1 <= choice <= len(exercises):
                return exercises[choice - 1][0]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")


# =========================
# WORKOUTS
# =========================

def getWorkoutInput(user_id):
    print(
        "\nAdd Workout Details "
        "(Example: 12/25/2026)"
    )

    workout_date = input(
        "Enter the workout date: "
    ).strip()

    notes = input(
        "Enter any notes for the workout: "
    ).strip()

    workout_id = addWorkout(
        user_id,
        workout_date,
        notes
    )

    print("Workout added successfully!")

    return workout_id


def chooseWorkout(user_id):
    workouts = getUserWorkouts(user_id)

    if not workouts:
        print("You have no workouts available.")
        return None

    print("\n--- Your Workouts ---")

    for number, workout in enumerate(
        workouts,
        start=1
    ):
        workout_date = workout[1]
        notes = workout[2]

        print(
            f"{number}. "
            f"{workout_date} - "
            f"{notes}"
        )

    while True:
        try:
            choice = int(
                input("Choose a workout: ")
            )

            if 1 <= choice <= len(workouts):
                return workouts[choice - 1][0]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")


def showRecentWorkout(user_id):
    workout = displayRecentWorkout(user_id)

    if not workout:
        print("No workouts found.")
        return

    print("\n--- Most Recent Workout ---")
    print(f"Date: {workout[1]}")
    print(f"Notes: {workout[2]}")


# =========================
# WORKOUT SETS
# =========================

def getSetNumber() -> int:
    while True:
        try:
            set_number = int(
                input("Enter Set Number: ")
            )

            if set_number <= 0:
                print(
                    "Set number must be greater than 0."
                )
                continue

            return set_number

        except ValueError:
            print("Please enter a valid number.")


def getWeight() -> float:
    while True:
        try:
            weight = float(
                input("Enter Weight in lbs: ")
            )

            if weight < 0:
                print("Weight cannot be negative.")
                continue

            return weight

        except ValueError:
            print("Please enter a valid number.")


def getReps() -> int:
    while True:
        try:
            reps = int(
                input("Enter Reps: ")
            )

            if reps <= 0:
                print("Reps must be greater than 0.")
                continue

            return reps

        except ValueError:
            print("Please enter a valid number.")


def getWorkoutSetInput(user_id):
    workout_id = chooseWorkout(user_id)

    if workout_id is None:
        return

    exercise_id = chooseExercise(user_id)

    if exercise_id is None:
        return

    set_number = getSetNumber()
    weight = getWeight()
    reps = getReps()

    set_id = addWorkoutSet(
        workout_id,
        exercise_id,
        set_number,
        weight,
        reps
    )

    print(
        f"Workout set added successfully! "
        f"Set ID: {set_id}"
    )


def chooseWorkoutSet(user_id):
    workout_id = chooseWorkout(user_id)

    if workout_id is None:
        return None

    workout_sets = getWorkoutSets(workout_id)

    if not workout_sets:
        print("This workout has no sets.")
        return None

    print("\n--- Workout Sets ---")

    for number, workout_set in enumerate(
        workout_sets,
        start=1
    ):
        set_id = workout_set[0]
        exercise_name = workout_set[1]
        set_number = workout_set[2]
        weight = workout_set[3]
        reps = workout_set[4]

        print(
            f"{number}. "
            f"{exercise_name} | "
            f"Set {set_number} | "
            f"{weight} lb x {reps}"
        )

    while True:
        try:
            choice = int(
                input("Choose a set: ")
            )

            if 1 <= choice <= len(workout_sets):
                return workout_sets[choice - 1][0]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")


# =========================
# LOGGED-IN MENU
# =========================

def loggedInMenu(user_id, username, password):

    while True:
        print("\n--- GymApp Menu ---")
        print("1. Show Account Details")
        print("2. Add Exercise")
        print("3. Add Workout")
        print("4. Add Workout Set")
        print("5. Show Recent Workout")
        print("6. Delete Exercise")
        print("7. Delete Workout")
        print("8. Delete Workout Set")
        print("9. Delete Account")
        print("10. Logout")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            displayAccountDetails(
                username,
                password
            )

        elif choice == "2":
            getExerciseInput(user_id)

        elif choice == "3":
            getWorkoutInput(user_id)

        elif choice == "4":
            getWorkoutSetInput(user_id)

        elif choice == "5":
            showRecentWorkout(user_id)

        elif choice == "6":
            exercise_id = chooseExercise(user_id)

            if exercise_id is None:
                continue

            if deleteExercise(
                user_id,
                exercise_id
            ):
                print("Exercise deleted successfully.")
            else:
                print("Exercise could not be deleted.")

        elif choice == "7":
            workout_id = chooseWorkout(user_id)

            if workout_id is None:
                continue

            if deleteWorkout(
                user_id,
                workout_id
            ):
                print("Workout deleted successfully.")
            else:
                print("Workout could not be deleted.")

        elif choice == "8":
            set_id = chooseWorkoutSet(user_id)

            if set_id is None:
                continue

            if deleteWorkoutSet(
                user_id,
                set_id
            ):
                print(
                    "Workout set deleted successfully."
                )
            else:
                print(
                    "Workout set could not be deleted."
                )

        elif choice == "9":
            confirmation = input(
                "Are you sure you want to "
                "delete your account? (yes/no): "
            ).strip().lower()

            if confirmation != "yes":
                print("Account deletion cancelled.")
                continue

            if deleteUser(user_id):
                print("Account deleted successfully.")
                return

            print("Account could not be deleted.")

        elif choice == "10":
            print("Logged out.")
            return

        else:
            print("Invalid option.")


# =========================
# MAIN MENU
# =========================

def main():
    create_database()

    while True:
        print("\n--- GymApp ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            createUser()

        elif choice == "2":
            username = getUsername()
            password = getPassword()

            if not checkLoginCredentials(
                username,
                password
            ):
                print(
                    "Invalid username or password."
                )
                continue

            user_id = getUserId(
                username,
                password
            )

            print("Login successful!")

            loggedInMenu(
                user_id,
                username,
                password
            )

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()