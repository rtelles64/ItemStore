# Demonstrating how we interact with SQLite
import sqlite3

connection = sqlite3.connect('data.db')
# REMEMBER: delete data.db each time you run so as to avoid errors

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')

# Populate database with user info
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# generate more users
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz'),
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# save changes
connection.commit()

# close connection
connection.close()
