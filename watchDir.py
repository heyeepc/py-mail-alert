import  time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from txt2mail import txt2mail

class MyHandler(FileSystemEventHandler):

    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            if event.src_path.endswith(".txt"):
                time.sleep(1)
                mail = txtmail()
                try:
                    mail.txt_send_mail(filename=event.src_path)
                except:
                    print("文本文件格式不正确")

    def on_modified(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            if event.src_path.endswith(".txt"):
                time.sleep(1)
                mail = txt2mail()
                try:
                    mail.txt_send_mail(filename=event.src_path)
                except:
                    print("文本格式不正确")

if __name__ == '__main__':
    observer = Observer()
    event_handler = FileSystemEventHandler()
    dir = "./"
    observer.schedule(event_handler, dir, False)
    print(f"当前监控的目录；{dir}")
    observer.start()
    observer.join()