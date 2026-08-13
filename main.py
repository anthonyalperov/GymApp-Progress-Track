from database import addUser, deleteUser
from database import create_database
from database import checkLoginCredentials

#This section is for creating a user and getting their information
def createUser() -> dict:
    while True:
        user = {}

        user["name"] = input("Enter your Name: ")
        user["age"] = getAge()
        user["weight"] = getWeight()
        user["username"] = getUsername()
        user["password"] = getPassword()

        if addUser(
            user["name"],
            user["age"],
            user["weight"],
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

def getWeight() -> float:
    while True:
        try:
            weight = float(input("Enter your Weight in Lbs: "))

            if weight <= 0:
                print("Weight must be more than 0. Please enter a valid weight.")
                continue

            return weight

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def getUsername() -> str:
    username = input("Enter your Username: ")
    return username

def getPassword() -> str:
    password = input("Enter your Password: ")
    return password







#Main function to initialize the database and create a user
def main():
    create_database()

    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Delete Account")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            createUser()

        elif choice == "2":
            username = getUsername()
            password = getPassword()

            if checkLoginCredentials(username, password):
                print("Login successful!")
                break
            else:
                print("Invalid username or password.")

        elif choice == "3":
            username = getUsername()
            deleteUser(username)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()


