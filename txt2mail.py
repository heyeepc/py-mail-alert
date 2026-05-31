import smtplib
import chardet
import os
import codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders


class TxtMail(object):
    def __init__(self, host=None, auth_user=None, auth_password=None):
        # 建议通过初始化参数传入，不要硬编码
        self.host = host or "smtp.qq.com"
        self.auth_user = auth_user or "xxxxx@qq.com"
        self.auth_password = auth_password or ""
        self.sender = self.auth_user  # 发件人通常就是认证用户

    def send_mail(self, subject, msg_str, receiver_list, attachment_list=None):
        message = MIMEMultipart()
        message["From"] = self.sender
        # To 字段在多个接收者时应为逗号分隔的字符串
        message["To"] = ",".join(receiver_list)
        message["Subject"] = Header(subject, "utf-8")

        # 正文
        message.attach(MIMEText(msg_str, "plain", "utf-8"))

        # 附件处理
        if attachment_list:
            for att in attachment_list:
                if not os.path.exists(att):
                    continue
                filename = os.path.basename(att)
                with open(att, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    # 处理中文文件名
                    part.add_header("Content-Disposition", f"attachment; filename={Header(filename, 'utf-8').encode()}")
                    message.attach(part)

        try:
            # SSL 连接
            smtp_obj = smtplib.SMTP_SSL(self.host, smtplib.SMTP_SSL_PORT)
            smtp_obj.login(self.auth_user, self.auth_password)
            smtp_obj.sendmail(self.sender, receiver_list, message.as_string())
            smtp_obj.quit()
            print("邮件发送成功")
        except Exception as e:
            print(f"邮件发送失败: {e}")

    def guess_charset(self, filename):
        try:
            with open(filename, "rb") as f:
                raw = f.read()
                if raw.startswith(codecs.BOM_UTF8):
                    return "utf-8-sig"
                result = chardet.detect(raw)
                return result["encoding"] or "utf-8"
        except:
            return "utf-8"

    def txt_send_mail(self, filename):
        if not os.path.exists(filename):
            print("数据文件不存在")
            return

        encoding = self.guess_charset(filename)
        with open(filename, "r", encoding=encoding) as f:
            lines = [line.rstrip('\r\n') for line in f.readlines()]

        if len(lines) < 3:
            print("TXT文件格式错误，至少需要包含：接收人、主题、正文")
            return

        # 逻辑：第1行接收者，第2行主题，后续为正文，最后一行尝试解析为附件
        recipient_list = lines[0].split(",")
        subject = lines[1]

        # 假设最后一行如果是路径则为附件，否则也是正文
        potential_attachments = lines[-1].split(",")
        attachment_list = []
        msg_end_index = len(lines)

        if all(os.path.exists(path.strip()) for path in potential_attachments):
            attachment_list = [path.strip() for path in potential_attachments]
            msg_end_index = -1

        msg_str = "\n".join(lines[2:msg_end_index])

        self.send_mail(subject, msg_str, recipient_list, attachment_list)


if __name__ == "__main__":
    mymail = TxtMail(auth_user="你的邮箱", auth_password="授权码")
    mymail.txt_send_mail(filename="./test.txt")






