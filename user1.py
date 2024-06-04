import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class P2PNode:
    def __init__(self, port, peers, key):
        self.port = port
        self.peers = peers
        self.key = key
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('172.17.0.7', self.port))

    def start(self):
        threading.Thread(target=self._listen).start()
        threading.Thread(target=self._send_messages).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            decrypted_data = self._decrypt(data)
            print(f"\nReceived '{decrypted_data}' from {addr}\nEnter a message: ", end = "")

    def _send_messages(self):
        while True:
            message = input("Enter a message: ")
            cipher_text = self._encrypt(message)
            for peer in self.peers:
                self.sock.sendto(cipher_text, peer)

    def _encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        cipher_text = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

        return cipher.iv + cipher_text

    def _decrypt(self, data):
        iv = data[:AES.block_size]
        cipher_text = data[AES.block_size:]
        decrypt_cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_text = unpad(decrypt_cipher.decrypt(cipher_text), AES.block_size)