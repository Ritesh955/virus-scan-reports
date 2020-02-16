from app import app
from services import helper_service
from datetime import datetime,timedelta

def insert_record(response):
    if len(response.values()) >1:
    	try:
	        conn = helper_service.get_db_connection()
	        cursor = conn.cursor()
	        cursor.execute(app.config['INSERT_STMT'],(response['resource'],response['detection_name'],response['number_of_engines'],response['scan_date'],datetime.now()))
	        #print("New record saved to database")
    	except Exception as e:
	    	print(e)
    	finally:
	        conn.commit()
	        conn.close()
    else:
        print("Invalid record. Did not save to database")

def update_record(response):
    if len(response.values()) >1:
    	try:
    		conn = helper_service.get_db_connection()
    		cursor = conn.cursor()
    		cursor.execute(app.config['UPDATE_STMT'],(response['detection_name'],response['number_of_engines'],response['scan_date'],datetime.now(),response['resource']))
    		#print("Existing record updated saved to database.")
    	except Exception as e:
	    	print(e)
    	finally:
	        conn.commit()
	        conn.close()
    else:
        print("Invalid record. Did not save to database")