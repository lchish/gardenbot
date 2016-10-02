import tornado.ioloop
import tornado.web
import tornado.websocket
import webview
import threading
import math
import time
import random
import json

PORT = 8888
SLEEP_TIME = 1

class MainHandler(tornado.web.RequestHandler):
    """
    Initialises and creates the web template
    """
    def get(self):
        self.render("index.html")

class JadensWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self,application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        self.writetobrowser = False

    def write_data(self):
        while self.writetobrowser:
            # Exercise for you overwrite the following with your own values
            # make the time be based off the users time
            #12:09PM on Sep 25, 2016
            datatosend = { 'temperature' : str(random.randrange(10,30)) + '°', 'date' : time.strftime("%I:%M on %b %d, %Y") }
            self.write_message(datatosend)
            time.sleep(SLEEP_TIME)

    def open(self):
        print("WebSocket opened")
        if not self.writetobrowser:
            self.writetobrowser = True
            writerthread = threading.Thread(target=self.write_data, daemon=True)
            writerthread.start()

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.write_message(u"Received message from browser: " + message)

    def on_close(self):
        self.writetobrowser = False
        print("WebSocket closed")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", JadensWebSocket),
    ])

def start_tornado():
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

def stop_tornado():
    tornado.ioloop.IOLoop.current().stop()

def start():
    try:
        tornado_thread = threading.Thread(target=start_tornado, daemon=True)
        tornado_thread.start()

        # You might want to remove the webview. I find it nice for debugging
        webview.create_window("It works, Jaden!", "http://127.0.0.1:8888", fullscreen = False)
    finally:
        webview.destroy_window()
        stop_tornado()

if __name__ == "__main__":
    start()
