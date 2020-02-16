import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def send_email(fromaddr,toaddr,passwd,filename,filePath):
        msg = MIMEMultipart() 
        msg['From'] = fromaddr 
        msg['To'] = toaddr
        msg['Subject'] = "Virus Scan Report"
        body = "Hello,  Please find the Virus Scan Report Attached. Thanks!"
        msg.attach(MIMEText(body, 'plain')) 
        attachment = open(filePath, "rb") 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        msg.attach(p) 
          
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        
        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(fromaddr, passwd) 
        text = msg.as_string() 
        s.sendmail(fromaddr, toaddr, text) 
        s.quit() 
