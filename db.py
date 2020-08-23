import sqlite3

connection = sqlite3.connect('ads.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE ads(id integer not null primary key, title text, description text, price integer, bids integer)")
cursor.execute("INSERT INTO ads VALUES (1, 'GeForce 1060', 'GDDR5', 150, 100)")
cursor.execute("INSERT INTO ads VALUES (2, 'Bike', 'Yamaha', 5000, 4000)")
cursor.execute("INSERT INTO ads VALUES (3, 'Ticket', 'Ticket to the ZOO', 50, 50)")

connection.commit()
connection.close()