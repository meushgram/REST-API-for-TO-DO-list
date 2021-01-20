from flask import Flask
import sqlite3
connection = sqlite3.connect("master.db")
cursor = connection.cursor()
# query = "CREATE TABLE toDoList (id INTEGER PRIMARY KEY, date text, toDo text)"
# cursor.execute(query)
# query = "INSERT INTO toDoList VALUES(?,?,?)"
# testData = [(None,"2016-01-01","Test1"),(None,"2016-01-01","Test2"),(None,"2016-01-01","Test3"),(None,"2016-01-01","Test4"),(None,"2016-01-01","Test5")]
# cursor.executemany(query,testData)
query = "CREATE TABLE users (username text,password text)"
cursor.execute(query)
query = "INSERT INTO users VALUES (?,?)"
cursor.execute(query,('dhanush','123'))
######
query = "SELECT * FROM users"
for row in cursor.execute(query):
    print(row)
connection.commit()
connection.close()