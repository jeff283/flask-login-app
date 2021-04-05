import sqlite3

def store():
	global conn
	global c
	conn = sqlite3.connect("database.db")
	c = conn.cursor()

	#creating a table
	c.execute("""CREATE TABLE IF NOT EXISTS login (
	  username TEXT,
	  password TEXT
	)
	          """)
store()