import mysql.connector
from services import helper_service

#TODO: check if mysql is installed on the system

try:
	conn = helper_service.get_db_connection()
	cursor = conn.cursor()
	# check if database exists
	cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
	#check if database table called cache exists
	cursor.execute("CREATE TABLE IF NOT EXISTS cache (hash_value VARCHAR(255) PRIMARY KEY,detection_name VARCHAR(255),number_of_engines INTEGER, scan_date TIMESTAMP, query_date TIMESTAMP NULL)")
except Exception as e:
	print(e)
finally:
	conn.commit()
	conn.close()