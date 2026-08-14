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

def deleteExercise(user_id, exercise_name):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM exercises
        WHERE user_id = ? AND exercise_name = ?
        """,
        (user_id, exercise_name)
    )

    connection.commit()
    connection.close()

def addWorkout(user_id, workout_date, notes):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workouts (user_id, workout_date, notes)
        VALUES (?, ?, ?)
        """,
        (user_id, workout_date, notes)
    )

    connection.commit()
    workout_id = cursor.lastrowid
    connection.close()
    return workout_id

def getUserWorkouts(user_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT workout_id, workout_date, notes
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_id DESC
        """,
        (user_id,)
    )

    workouts = cursor.fetchall()
    connection.close()

    return workouts

def deleteWorkout(user_id, workout_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM workouts
        WHERE workout_id = ? AND user_id = ?
        """,
        (workout_id, user_id)
    )

    connection.commit()
    connection.close()

def deleteWorkoutSet(user_id, set_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM workout_sets
        WHERE set_id = ?
        AND workout_id IN (
            SELECT workout_id
            FROM workouts
            WHERE user_id = ?
        )
        """,
        (set_id, user_id)
    )

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0


def displayRecentWorkout(user_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT workout_date, notes
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    recent_workout = cursor.fetchone()
    connection.close()

    if recent_workout:
        print("\n--- Most Recent Workout ---")
        print(f"Date: {recent_workout[0]}")
        print(f"Notes: {recent_workout[1]}")
    else:
        print("No workouts found.")

def getWorkoutSets(workout_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ws.set_id,
            e.exercise_name,
            ws.set_number,
            ws.weight,
            ws.reps
        FROM workout_sets ws
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        WHERE ws.workout_id = ?
        ORDER BY e.exercise_name, ws.set_number
        """,
        (workout_id,)
    )

    workout_sets = cursor.fetchall()

    connection.close()

    return workout_sets


def addWorkoutSet(workout_id, exercise_id, set_number, weight, reps):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workout_sets
        (workout_id, exercise_id, set_number, weight, reps)
        VALUES (?, ?, ?, ?, ?)
        """,
        (workout_id, exercise_id, set_number, weight, reps)
    )

    connection.commit()

    set_id = cursor.lastrowid

    connection.close()

    return set_id

def getUserExercises(user_id):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT exercise_id, exercise_name, muscle_group
        FROM exercises
        WHERE user_id = ?
        ORDER BY exercise_id
        """,
        (user_id,)
    )

    exercises = cursor.fetchall()
    connection.close()

    return exercises