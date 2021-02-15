import sqlite3
from config import DB_PATH

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("CREATE TABLE ads(id integer not null primary key, title text, description text, price integer, bids integer)")
cursor.execute("INSERT INTO ads VALUES (1, 'GeForce 1060', 'GDDR5', 150, 100)")
cursor.execute("INSERT INTO ads VALUES (2, 'Bike', 'Yamaha', 5000, 4000)")
cursor.execute("INSERT INTO ads VALUES (3, 'Ticket', 'Ticket to the ZOO', 50, 50)")

cursor.execute("CREATE TABLE users(id integer not null primary key, name text, password text)")
cursor.execute("INSERT INTO users VALUES (1, 'admin', 'test1234')")

connection.commit()
connection.close()
