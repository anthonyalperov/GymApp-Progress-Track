import sqlite3

def create_database():
    connection = sqlite3.connect("database/gym.db")
    with open("sql/schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


import sqlite3


def addUser(name, age, weight, username, password):
    connection = sqlite3.connect("database/gym.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (name, age, weight, username, password)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, age, weight, username, password)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


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
    