import mysql.connector

DB_COLUMNS = ['hash_value','detection_name','number_of_engines','scan_date','query_date']

# Returns Database Connection Object

def get_db_connection(db_name='mydatabase'):
    conn = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      db=db_name
    )
    return conn

# Yeild subsequent chunk of list (size n) every new call
def divide_chunks(l, n): 
   for i in range(0, len(l), n):  
       yield l[i:i + n]