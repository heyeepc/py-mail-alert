import poplib
from email.parser import BytesParser
from email.header import decode_header
from email.utils import parseaddr

email = ""
password = ""
pop3_server = ""

server = smtplib.poplib.POP3_SSL(pop3_server)

server.set_debuglevel(1)
print(server.getwelcome().decode('utf8'))

server.user(email)
server.pass_(password)

print("邮件数量 ：s个.大小：%.2fmb"%(server.stat()[0],server.stat()[1]/1024/1024))

