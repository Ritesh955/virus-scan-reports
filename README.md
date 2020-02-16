# Virus Scan Reports

In this project, we want to build a website that allows users to upload a text file as a list of hashes (MD5 or Sha256) and generates a simple report using information provided by querying VirusTotal's public API for the scan report of the hashes.<br>
 
<b>Q.</b> Many people might use the website frequently over time. The same hash can be queried multiple times. Consider how to store VirusTotal's results locally so that the website does not need to query the same hash again from VirusTotal if the scan date is less than 1 day ago.<br>
<b>A.</b> Assuming VirusTotal scans a particular resource(hash_value) atmost once in a day. Under that assumption the scan_date provided by VirusTotal for a resource(hash_value) should not change more than once in a day. Therefore, hitting virustotal api for the same resource multiple times a day doesnot make sense. We can use cache to prevent this from happening. Here we use MySql database as cache.<br>

# Cache Implementation:
  
  Create a table called cache in the database with fields:<br>
*  hash_value (primary key) 
   		- To save the hash_value sent by the user
*  detection_name 
   		- Fortinet dectection name sent by the VirusTotal API, specific to a hash_value
*  number_of_engines
   		- Number of engines that detected sent by the VirusToal API, specific to a hash_value 
*  scan_date (Timestamp)
   		- The scan_date sent by the VirusTotoal API, specific to a hash_value
*  query_timestamp (Timestamp)  
   	    - The last time we queired the Virtual API server.<br>
   	    - This field helps us to identify if we have already queried the VirusTotal API server in the last 24 hours. 
  
    <b>Update Policy:</b><br>
    For each hash_value we would first look into the cache table<br>
    if current_time - query_date < 24 hours:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;add the record to report <br>
    elif current_time - query_date > 24 hours in record present in cache:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;query the VirusTotal <br>
    &nbsp;&nbsp;&nbsp;&nbsp;save it to the cache <br>
    &nbsp;&nbsp;&nbsp;&nbsp;update the query_date <br>
    &nbsp;&nbsp;&nbsp;&nbsp;add the record to report <br>

    <b>Eviction Policy:</b>
     	 We run a cron job everynight at 12:00 AM to delete all records from the sqltable where current_time - query_date > 24.<br>

Steps: 
   1. Check if system requirements are met:<br>
      1a. Check if MySql(5.7.29)+ is installed <br>
      1b. Check if python3.6+ is installed on the system <br>
   2. Add configurations to app.py<br>
      2a. Setup a mailbox over which you can send an email.<br>
      2b. Set the password for the email. <br>
   3. Start service mysql start <br>
      service mysql start <br>
      create a new database using "CREATE IF NOT EXISTS mydatabase" <br>
   4. Run: python3 sql_scripts.py <br>
   5. Setup eviction cron_job to daily trigger the cache_eviction_cron_job.py <br>
   6. Start the server <br>
      - navigate to root of the directory and run python3 main.py <br>


Technology Stack:<br>
  1. Flask<br>
  2. Python<br>
  3. MySQL <br>
  4. Linux <br>

Requeried dependecies:
  flask<br>
  mysql.connector <br>
  datetime <br>
  json <br>
  requests <br>
  fpdf <br>
  smtplib <br>
  email.mime.multipart<br>
  email.mime.text<br>
  email.mime.base<br>
  email<br>

  
<b>Q.</b> The input list could be very large. So users may not be able to wait for
the queries to complete, and as such, could not see the report right away.
Consider how to let users come back later to see the report.<br>

<b>A.</b> Since we will be using VirusTotal Public Api for this project and same is limited to 4 requests per minute for one API Key. This is a bottleneck in report creation process. Not much can be done to speed up the report generation. We need to wait for 1 min before we make another four requests to the API Server. Due to the same reason the time user would have to wait before he can see the report is (#hash_values/4) minutes. For 100 hash_value inputs if we are starting the server the first time and cache would not have not any effect as its empty. Therefore we decided to develop a email service to send reports to user's emails upon completion. He or she doesn't need to wait for the process to finish. He or she would be notified onces it's finished. Sending an email's to the user throgh a generic account is the main idea.

<b>Q.</b> What would be eviction policy for cache?
<b>A</b> One of the columns in the cache table saves the query timestamp for each hash_value as discussed in the cache implementation. We need to delete records which haven't been queried for more than 1 day now. As these again need to be queried from the server. Therefore we delete all the records where curr_time-query_time > 24 hours. This clean up would make the implementation of the cache more efficient and faster.











   
