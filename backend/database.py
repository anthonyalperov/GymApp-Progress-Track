import sqlite3
from pathlib import Path
import os


# =========================
# APPLICATION PATHS
# =========================

APP_DATA_DIR = (
    Path(os.getenv("LOCALAPPDATA"))
    / "GymApp"
)

APP_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = (
    APP_DATA_DIR
    / "gym.db"
)


BACKEND_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BACKEND_DIR.parent

SCHEMA_PATH = (
    PROJECT_ROOT
    / "sql"
    / "schema.sql"
)


# =========================
# DATABASE CONNECTION
# =========================

def getConnection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def create_database():
    connection = getConnection()

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


# =========================
# USERS
# =========================

def addUser(name, age, bodyweight, username, password):
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (name, age, bodyweight, username, password)
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
    connection = getConnection()
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


def checkLoginCredentials(username, password):
    return getUserId(username, password) is not None


def showAccountDetails(username, password):
    connection = getConnection()
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

    return user


def deleteUser(user_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0


# =========================
# EXERCISES
# =========================

def addExercise(user_id, exercise_name, muscle_group):
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO exercises
            (user_id, exercise_name, muscle_group)
            VALUES (?, ?, ?)
            """,
            (user_id, exercise_name, muscle_group)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def getUserExercises(user_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT exercise_id, exercise_name, muscle_group
        FROM exercises
        WHERE user_id = ?
        ORDER BY exercise_name
        """,
        (user_id,)
    )

    exercises = cursor.fetchall()

    connection.close()

    return exercises


def deleteExercise(user_id, exercise_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM exercises
        WHERE exercise_id = ?
        AND user_id = ?
        """,
        (exercise_id, user_id)
    )

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0


# =========================
# WORKOUTS
# =========================

def addWorkout(user_id, workout_date, notes):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workouts
        (user_id, workout_date, notes)
        VALUES (?, ?, ?)
        """,
        (user_id, workout_date, notes)
    )

    connection.commit()

    workout_id = cursor.lastrowid

    connection.close()

    return workout_id


def getUserWorkouts(user_id):
    connection = getConnection()
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
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM workouts
        WHERE workout_id = ?
        AND user_id = ?
        """,
        (workout_id, user_id)
    )

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0


def displayRecentWorkout(user_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT workout_id, workout_date, notes
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    recent_workout = cursor.fetchone()

    connection.close()

    return recent_workout


# =========================
# WORKOUT SETS
# =========================

def addWorkoutSet(workout_id, exercise_id, set_number, weight, reps):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO workout_sets
        (workout_id, exercise_id, set_number, weight, reps)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            workout_id,
            exercise_id,
            set_number,
            weight,
            reps
        )
    )

    connection.commit()

    set_id = cursor.lastrowid

    connection.close()

    return set_id


def getWorkoutSets(workout_id):
    connection = getConnection()
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


def deleteWorkoutSet(user_id, set_id):
    connection = getConnection()
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

#========================
# GRAPH DATA
#========================

def getWeeklyMuscleGroupFrequency(user_id, start_date, end_date):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            e.muscle_group,
            COUNT(DISTINCT w.workout_id)
        FROM workouts w
        JOIN workout_sets ws
            ON w.workout_id = ws.workout_id
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        WHERE w.user_id = ?
        AND w.workout_date BETWEEN ? AND ?
        GROUP BY e.muscle_group
        ORDER BY e.muscle_group
        """,
        (user_id, start_date, end_date)
    )

    data = cursor.fetchall()

    connection.close()

    return data


def getExerciseHistory(user_id, exercise_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            w.workout_date,
            ws.weight,
            ws.reps
        FROM workout_sets ws
        JOIN workouts w
            ON ws.workout_id = w.workout_id
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        WHERE w.user_id = ?
        AND e.exercise_id = ?
        ORDER BY w.workout_date
        """,
        (user_id, exercise_id)
    )

    data = cursor.fetchall()

    connection.close()

    return data


def getUserBodyweight(user_id):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT bodyweight
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return user[0]

    return None