import mysql.connector

# Returns Database Connection Object
conn = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database = "mydatabase"
)

cursor = conn.cursor()
cursor.execute("Delete from cache where TIMESTAMPDIFF(HOUR,query_date,now()) > 24")
conn.commit()
conn.close()


