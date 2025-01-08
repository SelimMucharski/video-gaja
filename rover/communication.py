import socket
import threading

class Socket_Server:
    def __init__(self, ip_addr: str, port: int):
        self.mail_box: list[bytes] = []
        self.conn = None
        self.init_socket(ip_addr, port)
        self.thread = threading.Thread(target=self.thread_fun)
        self.thread.start()

    def init_socket(self, ip_addr, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip_addr, port))
        self.socket.listen()
        print(f'Listening on port {port}')


    def thread_fun(self):
        while True:
            if not self.conn:
                self.conn, addr = self.socket.accept()
                print(f'Connected with {addr}')
                continue

            data = self.conn.recv(1024)
            if not data:
                print(f'Disconnected')
                self.mail_box = []
                self.conn.close()
                self.conn = None
                continue

            self.mail_box.append(data)

    def send(self, data: bytes):
        if not self.conn: return
        self.conn.sendall(data)

    def connected(self) -> bool:
        return False if self.conn is None else True

    def __del__(self):
        if self.conn: self.conn.close()
        self.socket.close()