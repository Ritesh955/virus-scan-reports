from flask import Flask

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = './resources'
app.config['FILE_NAME'] = 'hash_input'
app.config['VIRUS_TOTAL_API'] = 'https://www.virustotal.com/vtapi/v2/file/report'
app.config['API_KEY'] = '5ffd4e50fa707fe34dadf96a31dac0160aa9b7848b5b9a921ed9fe0d4267c1d0'
app.config['INSERT_STMT'] = """INSERT into cache (hash_value , detection_name, number_of_engines, scan_date, query_date) VALUES (%s,%s,%s,%s,%s)""" 
app.config['UPDATE_STMT'] = """UPDATE cache set detection_name=%s, number_of_engines=%s, scan_date=%s, query_date=%s where hash_value = %s"""
app.config['GENERIC_EMAIL'] = 'noreplyreporting268@gmail.com'
app.config['PASSWD'] = 'noreporting67'