from database import addUser, deleteUser, showAccountDetails, getUserId, addExercise
from database import create_database
from database import checkLoginCredentials

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
        choice = input("Choose a muscle group: ")

        if choice in muscle_groups:
            muscle_group = muscle_groups[choice]
            break

        print("Invalid muscle group.")

    addExercise(user_id, exercise_name, muscle_group)

    print(f"{exercise_name} added successfully!")

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
                    "Choose an option: "
                )

                if choice2 == "1":
                    showAccountDetails(username, password)

                elif choice2 == "2":
                    deleteUser(username)

                elif choice2 == "3":
                    user_id = getUserId(username, password)
                    getExerciseInput(user_id)

                else:
                    print("Invalid option.")

            else:
                print("Invalid username or password.")

        elif choice == "3":
            username = getUsername()
            password = getPassword()

            if checkLoginCredentials(username, password):
                showAccountDetails(username, password)
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


