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

