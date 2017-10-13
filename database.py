#!/usr/bin/python
#Code partly from https://www.tutorialspoint.com/python/python_database_access.htm
import MySQLdb




def connectAndGetCursor():
	# Open database connection
	db = MySQLdb.connect("localhost","testuser","pwd","testdb" )
	#Get cursor
	cursor = db.cursor()
	return db, cursor

def executeSQL(sql):
	db, cursor = connectAndGetCursor()	
	cursor.execute(sql)
	db.close()

def eraseResults():
	sql = "DROP TABLE IF EXISTS RESULTS"
	executeSQL(sql)
	
def createResults():
	sql = """CREATE TABLE RESULTS (
			ANGLE FLOAT,
			VELOCITY FLOAT,
			PRESSURE FLOAT)"""
	executeSQL(sql)

def insert(angle, velocity, pressure):
	#TODO Check valid input?
	db, cursor = connectAndGetCursor()
	sql = "INSERT INTO RESULTS (ANGLE, VELOCITY, PRESSURE) VALUES ('" + str(angle) + "','" + str(velocity) + "','" + str(pressure) + "')"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
		print('Error')
	db.close()

def readValues(angle):
	#TODO Check valid input?
	db, cursor = connectAndGetCursor()
	sql = "SELECT * FROM RESULTS WHERE CAST(ANGLE AS DECIMAL) = CAST(" + str(angle) + " AS DECIMAL)"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			velocity = row[1]
			pressure = row[2]
		return velocity, pressure
	except:	 
		print "Unable to read data/No such angle in DB"
		return -1, -1
	db.close()