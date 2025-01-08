import socket
import threading
import json
import evdev
import cv2, socket, numpy, pickle

data = {"speedLeft": 0, "speedRight": 0}
inputs = {"ABS_RY": 0, "ABS_Y": 0, 'ABS_RX': 0}

def send_command():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(('192.168.5.1', 2137))
            while True:
                if data:
                    s.sendall(json.dumps(data).encode())

                    result = s.recv(1024)
                    jresult = json.loads(result.decode())
                    if not jresult['result']: break
        except ConnectionRefusedError:
            print('Cannot connect to rover')
        except Exception as e:
            print(e)

def get_inputs():
    for event in evdev.InputDevice("/dev/input/event15").read_loop():
        if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_RY:
                    inputs['ABS_RY'] = event.value
                    # data['speedRight'] = -event.value/32768*100
                if event.code == evdev.ecodes.ABS_Y:
                    inputs['ABS_Y'] = event.value
                    # data['speedLeft'] = -event.value/32768*100
                if event.code == evdev.ecodes.ABS_RX:
                    inputs['ABS_RX'] = event.value
                    # data['speedLeft'] = -event.value/32768*100

def recv_video():
    s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    ip="192.168.5.5"
    port=2323
    s.bind((ip,port))

    while True:
        x=s.recvfrom(100000000)
        # print(x)
        clientip = x[1][0]
        data=x[0]
        data=pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('Gaja Video', data)
        if cv2.waitKey(10) == 13:
            break
    cv2.destroyAllWindows()


CommandSender = threading.Thread(target=send_command)
CommandSender.start()

InputsGetter = threading.Thread(target=get_inputs)
InputsGetter.start()

VideoRecv = threading.Thread(target=recv_video)
VideoRecv.start()

while True:
    linVel = -inputs['ABS_RY']/32768*150
    rotVel = -inputs['ABS_RX']/32768*150

    data['speedLeft'] = linVel - rotVel
    data['speedRight'] = linVel + rotVel

    if(abs(data['speedLeft']) < 10): data['speedLeft'] = 0
    if(abs(data['speedRight']) < 10): data['speedRight'] = 0

    # print(data['speedLeft'], data['speedRight'])
    pass
