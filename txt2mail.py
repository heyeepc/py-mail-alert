import smtplib
import chardet
import os
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.multipart import MIMEMultipart

class txtmail(object):
    def __init__(self,host=None,auth_user=None,auth_password=None):
        self.host = "smtp.qq.com" if host is None else host
        self.auth_user = auth_user = "xxxxx" if auth_user is None else auth_user

        self.auth_password = "" if auth_password is None else auth_password
        self.sender = ""

    def send_mail(self,subject,msg_str,receiver_list):

        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = Header(",".join(receiver_list),"utf-8")
        message["Subject"] = Header(subject,"utf-8")
        message.attach(MIMEText(msg_str,"plain","utf-8"))
        
        if attachment:
            for att in attachment_list:
                attachment = MIMEBase(open(att,"rb").read(),"base64","utf-8")
                attachment["Content-Type"] = "application/octet-stream"
                attachment=att.split("/")[-1]

                filename=os.path.basename(att)

                attachment.add_header("Content-Disposition","attachment",filename=("utf-8","",filename))
                message.attach(attachment)







