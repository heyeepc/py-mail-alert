import  time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from txt2mail import txt2mail

class MyHandler(FileSystemEventHandler):
    