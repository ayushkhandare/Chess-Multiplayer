import socket
import pickle
import time

class Network:
    def decode_ip(hex_code):
        octets = [str(int(hex_code[i:i+2], 16)) for i in range(0, len(hex_code), 2)]
        return '.'.join(octets)
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ip = input("Enter other player's code: ")
        self.host = Network.decode_ip(client_ip)
        self.port = 5555
        self.addr = (self.host, self.port)
        self.board = self.connect()
        self.board = pickle.loads(self.board)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(4096*8)

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        """
        :param data: str
        :return: str
        """
        start_time = time.time()
        while time.time() - start_time < 5:
            try:
                if pick:
                    self.client.send(pickle.dumps(data))
                else:
                    self.client.send(str.encode(data))
                reply = self.client.recv(4096*8)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


