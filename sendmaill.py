import poplib
from email.parser import BytesParser
from email.header import decode_header

# 1. 配置信息（以QQ邮箱为例，POP3服务器为 pop.qq.com）
email = "你的邮箱@qq.com"
password = "你的POP3授权码"  # 注意：通常不是登录密码，而是授权码
pop3_server = "pop.qq.com"

# 2. 连接到 POP3 服务器
# 直接使用 poplib.POP3_SSL
server = poplib.POP3_SSL(pop3_server, port=995)

# 显示调试信息（1开启，0关闭）
server.set_debuglevel(1)
print(server.getwelcome().decode('utf-8'))

# 3. 身份验证
server.user(email)
server.pass_(password)

# 4. 获取邮箱状态 (邮件数量, 邮箱大小)
email_count, mailbox_size = server.stat()
print("邮件数量：%d 个. 总大小：%.2f MB" % (email_count, mailbox_size / 1024 / 1024))

# 5. 读取最新的一封邮件 (index = email_count)
if email_count > 0:
    index = email_count  # 邮件索引从 1 开始，所以最后总数就是最新一封

    # server.retr(index) 返回: (状态码, 邮件文本每行的二进制列表, 邮件大小)
    resp, lines, octets = server.retr(index)

    # 将二进制行列表拼接成一个完整的字节流
    mail_bytes = b'\r\n'.join(lines)

    # 使用 BytesParser 解析邮件
    msg = BytesParser().parsebytes(mail_bytes)


    # 6. 辅助解码函数
    def decode_str(s):
        if not s:
            return ""
        value, charset = decode_header(s)[0]
        if isinstance(value, bytes):
            if charset:
                value = value.decode(charset)
            else:
                value = value.decode('utf-8', errors='ignore')
        return value


    print("\n" + "=" * 30 + " 解析结果 " + "=" * 30)
    print("邮件主题:", decode_str(msg['Subject']))
    print("发件人:", decode_str(msg['From']))


    # 7. 递归解析邮件正文 (处理单部分或多部分邮件)
    def get_mail_content(message):
        content = ""
        if message.is_multipart():
            # 如果是多部分，遍历每一部分
            for part in message.walk():
                content_type = part.get_content_type()
                # 我们通常只取纯文本部分
                if content_type == 'text/plain':
                    charset = part.get_content_charset() or 'utf-8'
                    content += part.get_payload(decode=True).decode(charset, errors='ignore')
        else:
            # 如果是单部分邮件
            charset = message.get_content_charset() or 'utf-8'
            content = message.get_payload(decode=True).decode(charset, errors='ignore')
        return content


    print("邮件内容:\n", get_mail_content(msg))
    print("=" * 70)

    # 8. 删除邮件逻辑 (注意：取消注释后，运行会真的在服务器删除这封邮件！)
    # server.dele(index)
    # print(f"已标记删除第 {index} 封邮件")

else:
    print("邮箱里没有邮件。")

# 9. 退出服务器（真正执行删除是在 quit 时）
server.quit()