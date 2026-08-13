import sqlite3

#This section is for filling in SQL database with user information and retrieving it when needed


#This section is for creating the database and adding users to it
def create_database():
    connection = sqlite3.connect("database/gym.db")
    with open("sql/schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

def addUser(name, age, bodyweight, username, password):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (name, age, bodyweight, username, password)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, age, bodyweight, username, password)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()

def getUserId(username, password):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return user[0]

    return None

def deleteUser(username):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (username,)
    )

    connection.commit()
    connection.close()

def checkLoginCredentials(username, password):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user is not None

def showAccountDetails(username: str, password: str) -> None:

    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id, name, age, bodyweight, username
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        print("\n--- Account Details ---")
        print(f"User ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Age: {user[2]}")
        print(f"Body Weight: {user[3]} lb")
        print(f"Username: {user[4]}")
    else:
        print("Account not found.")

#This section is for inputing exercises
def addExercise(user_id, exercise_name, muscle_group):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO exercises (user_id, exercise_name, muscle_group)
        VALUES (?, ?, ?)
        """,
        (user_id, exercise_name, muscle_group)
    )

    connection.commit()
    connection.close()


    #Muscle Groups I hit:
    # Chest
    # Back
    # Legs
    # Arms
    # Shoulders
    # Abs