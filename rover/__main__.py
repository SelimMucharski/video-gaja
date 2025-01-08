#!/usr/bin/env python3

import RPi.GPIO as GPIO # type: ignore
from robot import Robot
from communication import Socket_Server
import threading
import json

ROVER_IP = "192.168.5.1"
CONTROLLER_IP = "192.168.5.5"
VIDEO_PORT = 2323
COMMAND_PORT = 2137

def sendVideo():
    import cv2, socket, pickle

    s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip= CONTROLLER_IP
    serverport= VIDEO_PORT

    cap = cv2.VideoCapture(0)

    while True:
        ret, photo = cap.read()
        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY),30])
        x_as_bytes = pickle.dumps(buffer)
        s.sendto(x_as_bytes,(serverip , serverport))
        # print(x_as_bytes)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    server = Socket_Server(ROVER_IP, COMMAND_PORT)
    robot = Robot()

    SendingVideo = threading.Thread(target=sendVideo)
    SendingVideo.start()

    try:
        while True:
            # print(server.conn)
            if not server.mail_box: continue
            if not server.connected():
                robot.set_speed(0, 0) # nie działa
                break

            data = server.mail_box.pop(0)
            print(f'Got {data}')
            jdata = json.loads(data.decode())

            speedLeft = jdata['speedLeft']
            speedRight = jdata['speedRight']
            # print(speedLeft, speedRight)

            robot.set_speed(speedLeft=speedLeft, speedRight=speedRight)
            server.send(json.dumps({"result": 1}).encode())
            pass
    except Exception as e:
        print(e)
