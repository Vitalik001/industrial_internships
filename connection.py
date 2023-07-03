from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password='new_password',
        database="industrial_internships3",
    ) as connection:
        print(connection)
except Error as e:
    print(e)

def send_view_query(connection, query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result, True
    except Error as e:
        print(e)
        return e, False


def send_modifying_query(connection, query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        print(e)
        return e