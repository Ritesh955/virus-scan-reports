import mysql.connector
import requests
import json
from datetime import datetime,timedelta
from app import app
from services import sql_service
from services import helper_service

def query_server(value,update_flag =0):
    url = app.config['VIRUS_TOTAL_API']
    params = {'apikey': app.config['API_KEY'], 'resource': value}
    try:    
	    response = requests.get(url, params=params)
	    answer = json.loads(response.text)
	    result = {}
	    result['resource']=value
	    result['detection_name'] = answer['scans']['Fortinet']['result']
	    result['number_of_engines'] = answer['positives']
	    result['scan_date'] = answer['scan_date']
	    if update_flag == 1:
	    	sql_service.update_record(result)
	    else:
	    	sql_service.insert_record(result)
	    return result
    except Exception as e:
	    print(e)

def query_database(value):
    select_sql = "select * from cache where hash_value ='"+value+"'"
    try:
	    conn = helper_service.get_db_connection()
	    cursor = conn.cursor()
	    cursor.execute(select_sql)
	    records = cursor.fetchall()  
	    if len(records) == 1:
	    	#print("Result Found in database")
	    	result = [item for item in records[0]]
	    	response = dict(zip(helper_service.DB_COLUMNS,list(result)))
	    	if (datetime.now()-records[0][4]).days < 1:
	    		return response
	    	else:
	    		return {'update_flag':1, 'value': value}
	    else:
	    	#print("Result not found in database. Therefore querying api server")
	    	return {'update_flag': 0 , 'value': value}
    except Exception as e: 
	    print(e)
    finally:
	    conn.commit()
	    conn.close()
