import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# 1. 修正导入：从 txt2mail 模块导入 TxtMail 类
from txt2mail import TxtMail


class MyHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        # 建议在这里统一配置好邮件客户端，避免每次修改文件都重新实例化
        self.mail_client = TxtMail(auth_user="你的邮箱@qq.com", auth_password="你的授权码")

    def process_txt(self, file_path):
        """抽取公共的监控处理逻辑"""
        if file_path.endswith(".txt"):
            print(f"检测到TXT文件变动: {file_path}")
            # 稍微等待文件写入完成，防止读取时文件正在被占用
            time.sleep(1)
            try:
                self.mail_client.txt_send_mail(filename=file_path)
            except Exception as e:
                print(f"发送失败或文本格式不正确: {e}")

    def on_moved(self, event):
        if not event.is_directory:
            # move 事件的目标路径是 dest_path
            self.process_txt(event.dest_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_txt(event.src_path)


if __name__ == '__main__':
    observer = Observer()
    # 2. 修正绑定：使用你自定义的 MyHandler
    event_handler = MyHandler()
    watch_dir = "./"

    observer.schedule(event_handler, watch_dir, recursive=False)
    print(f"当前正在监控目录: {watch_dir} ... (按 Ctrl+C 退出)")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()