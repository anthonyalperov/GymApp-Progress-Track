from database import (
    addUser,
    deleteUser,
    displayRecentWorkout,
    showAccountDetails,
    getUserId,
    getUserWorkouts,
    addExercise,
    addWorkout,
    addWorkoutSet,
    getUserExercises,
    create_database,
    checkLoginCredentials
)

#This section is for creating a user and getting their information
def createUser() -> dict:
    while True:
        user = {}

        user["name"] = input("Enter your Name: ")
        user["age"] = getAge()
        user["bodyweight"] = getBodyweight()
        user["username"] = getUsername()
        user["password"] = getPassword()

        if addUser(
            user["name"],
            user["age"],
            user["bodyweight"],
            user["username"],
            user["password"]
        ):
            print("Account created successfully!")
            return user

        print("That username already exists. Please try again.")

def getAge() -> int:
    while True:
        try:
            age = int(input("Enter your Age: "))

            if age <= 0:
                print("Age must be more than 0. Please enter a valid age.")
                continue

            return age

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def getBodyweight() -> float:
    while True:
        try:
            bodyweight = float(input("Enter your Body Weight in Lbs: "))

            if bodyweight <= 0:
                print("Body weight must be more than 0. Please enter a valid body weight.")
                continue

            return bodyweight

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def getUsername() -> str:
    username = input("Enter your Username: ")
    return username

def getPassword() -> str:
    password = input("Enter your Password: ")
    return password

def getExerciseInput(user_id):
    exercise_name = input("Enter the exercise name: ").strip()

    muscle_groups = {
        "1": "Chest",
        "2": "Back",
        "3": "Legs",
        "4": "Arms",
        "5": "Shoulders",
        "6": "Abs"
    }

    while True:
        print("\nMuscle Groups:")
        for key, value in muscle_groups.items():
            print(f"{key}. {value}")
        choice = input("Choose a muscle group: ")

        if choice in muscle_groups:
            muscle_group = muscle_groups[choice]
            break

        print("Invalid muscle group.")

    addExercise(user_id, exercise_name, muscle_group)

    print(f"{exercise_name} added successfully!")

def getWorkoutInput(user_id):
    print("Add Workout Details: Example: 12/25/2026")
    workout_date = input("Enter the workout date: ").strip()
    notes = input("Enter any notes for the workout: ").strip()

    workout_id = addWorkout(user_id, workout_date, notes)

    print(f"{workout_date} added successfully!")

    return workout_id

def getWorkoutSetInput(user_id):

    # Display workouts
    workouts = getUserWorkouts(user_id)

    if not workouts:
        print("You have no workouts.")
        return

    print("\n--- Your Workouts ---")

    for workout in workouts:
        print(
            f"Workout ID: {workout[0]} | "
            f"Date: {workout[1]} | "
            f"Notes: {workout[2]}"
        )

    workout_id = int(input("\nEnter Workout ID: "))


    # Display exercises
    exercises = getUserExercises(user_id)

    if not exercises:
        print("You have no exercises.")
        return

    print("\n--- Your Exercises ---")

    for exercise in exercises:
        print(
            f"Exercise ID: {exercise[0]} | "
            f"{exercise[1]} | "
            f"{exercise[2]}"
        )

    exercise_id = int(input("\nEnter Exercise ID: "))


    # Get set information
    set_number = int(input("Enter Set Number: "))
    weight = float(input("Enter Weight in lbs: "))
    reps = int(input("Enter Reps: "))


    addWorkoutSet(
        workout_id,
        exercise_id,
        set_number,
        weight,
        reps
    )

    print("Workout set added successfully!")



def chooseWorkout(user_id):
    workouts = getUserWorkouts(user_id)

    if not workouts:
        print("You have no workouts available.")
        return None

    print("\n--- Your Workouts ---")

    for number, workout in enumerate(workouts, start=1):
        workout_id = workout[0]
        workout_date = workout[1]
        notes = workout[2]

        print(f"{number}. {workout_date} - {notes}")

    while True:
        try:
            choice = int(input("Choose a workout: "))

            if 1 <= choice <= len(workouts):
                selected_workout = workouts[choice - 1]

                return selected_workout[0]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")


def chooseExercise(user_id):

    exercises = getUserExercises(user_id)

    if not exercises:
        print("You have no exercises available.")
        return None

    print("\n--- Your Exercises ---")

    for number, exercise in enumerate(exercises, start=1):
        print(f"{number}. {exercise[1]}")

    while True:
        try:
            choice = int(input("Choose an exercise: "))

            if 1 <= choice <= len(exercises):
                selected_exercise = exercises[choice - 1]
                return selected_exercise[0]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")
#Main function to initialize the database and create a user
def main():
    create_database()

    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Show Account Details")
        print("4. Delete Account")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            createUser()

        elif choice == "2":
            username = getUsername()
            password = getPassword()

            if checkLoginCredentials(username, password):
                print("Login successful!")

                choice2 = input(
                    "\n1. Show Account Details\n"
                    "2. Delete Account\n"
                    "3. Add Exercise\n"
                    "4. Add Workout\n"
                    "5. Add Workout Set\n"
                    "Choose an option: "
                )

                if choice2 == "1": #Show account details
                    showAccountDetails(username, password)

                elif choice2 == "2": #Delete account
                    deleteUser(username)

                elif choice2 == "3": #Add exercise
                    user_id = getUserId(username, password)
                    getExerciseInput(user_id)
                    displayRecentWorkout(user_id)

                elif choice2 == "4":
                    user_id = getUserId(username, password)

                    workout_id = getWorkoutInput(user_id)

                    print(f"Workout ID: {workout_id}")

                    displayRecentWorkout(user_id)

                elif choice2 == "5":
                    user_id = getUserId(username, password)
                    getWorkoutSetInput(user_id)
                    displayRecentWorkout(user_id)


                else:
                    print("Invalid option.")

            else:
                print("Invalid username or password.")

        elif choice == "3":
            username = getUsername()
            password = getPassword()

            if checkLoginCredentials(username, password):
                showAccountDetails(username, password)
                user_id = getUserId(username, password)
                displayRecentWorkout(user_id)
            else:
                print("Invalid username or password.")

        elif choice == "4":
            username = getUsername()
            deleteUser(username)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()


