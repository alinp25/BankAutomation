#Import OpenCV for image processing
#Import Time
import cv2, time
import sys
import os
import requests
import json

#Import entire tkinter for GUI widget creation
from tkinter import *


flag = 0
prev_w = 0
prev_h = 0

endtime = 0

# poti sa faci un stat pe fisier ca sa te duci direct la imaginea pe care o vrei
# si sa luam de acolo doar cele mai mari imagini
def videoFaceDet(subject_name):
    global flag
    global prev_w
    global prev_h
    video = cv2.VideoCapture(0)
    faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    if not(os.path.isdir(subject_name)):
        os.mkdir(subject_name)

    global endtime
    while True:
        check, frame = video.read()
        grayImg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(grayImg, scaleFactor=1.15, minNeighbors=6)
        name = subject_name
        for x, y, w, h in faces:
            if (h < 150 or w < 150): 
                    pass
            flag += 1
            cv2.imwrite(name + "/" + name + str(flag) + ".png",frame[y : (y + h), x: (x+w)])
        cv2.imshow("Capturing", frame)

        key=cv2.waitKey(1)
        # if key==ord('q'):
        #     break
        # endtime = time.time() + 60
        print(str(time.time()) + " " + str(endtime))
        if time.time() >= endtime:
            break
    cv2.destroyAllWindows()
    video.release()

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import *

name = ""

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        payload = '{"paths": "test"}'
        self.send_response(200)
        self.wfile.write(payload.encode(encoding='utf_8'))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        global name
        global endtime


        self._set_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len))
        
        name = post_body['name']
        endtime = time.time() + 5
        res = func_det_face()
        payload = '{"paths":' + str(res) + '}'
        self.send_response(200)
        self.wfile.write(payload.encode(encoding='utf_8'))
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def func_det_face():
    # run(port=8080)
    global name
    videoFaceDet(name)
    dict = {}

    for i in os.listdir(name):
        ## pisica schimba si tu slash 
        ## TODO
        dict[name + "\\" + i] = os.path.getsize(name + "\\" + i)

    dict =  sorted(dict.items(), key=lambda x: x[1],reverse=True)
    dict1 = dict[:20]
    dict = dict[20:]
    for i in dict:
        os.remove (i[0])
    dict = list(map(lambda x: x[0], dict1))
    print(dict)

    lst = list(map(lambda x: os.path.abspath(".") + "\\" + x, dict))
    print(lst)
    return lst



# func_det_face()
run()
