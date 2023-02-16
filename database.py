import psycopg2


connection = psycopg2.connect(
    host='127.0.0.1',
    user = 'postgres',
    password = 'postgres',
    db_name = 'bot_vk'
)

connection.autocommit = True


def create_table_search_users():
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                user_id_search VARCHAR(50) NOT NULL PRIMARY KEY;"""
        )
    print("[INFO] Table USERS was created.")
    return


def insert_search_users(user_id_search):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (user_id_search) 
            VALUES ('{user_id_search}');"""
        )
    return