import socket
import threading

class P2PNode:
    def __init__(self, port, peers):
        self.port = port
        self.peers = peers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('172.17.0.9', self.port))

    def start(self):
        threading.Thread(target=self._listen).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(f"Received {data} from {addr}")


if __name__ == '__main__':
    port = 8001
    peers = [('172.17.0.7', 8001), ('172.17.0.8', 8001)]
    node = P2PNode(port, peers)
    node.start()