import socket
import threading
import logging


class Server:
    def __init__(self):
        """
        Initialize the server with the IP and port number
        """
        self.ip = "127.0.0.1"
        self.port = 4444
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(5)
        print(f"[*] Listening on {self.ip}:{self.port}")
        self.clients = []
        self.nicknames = []
        logging.basicConfig(filename='chat.log', level=logging.INFO, format='%(asctime)s %(message)s')

    
    def broadcast(self, message:str):
        """

        Args:
            message (str): Message to be sent to all the clients

            send the message to all the clients
        """
        for client in self.clients:
            client.send(message)
        
    def handle_client(self, client:socket.socket):
        """
        Args:
            client (socket): Client socket object

            Handle the client connection
        """
        while True:
            try:
                message = client.recv(1024)
                logging.info(f"[*] Message received: {message.decode('utf-8')}")
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} left the chat!".encode("utf-8"))
                self.nicknames.remove(nickname)
                break
    
    def receive(self):
        """
        Receive the client connection and start the thread and save all messages in logfile

        """
        while True:
            try:
                client, address = self.server.accept()
                client.send("NICK".encode("utf-8"))
                nickname = client.recv(1024).decode("utf-8")
                self.nicknames.append(nickname)
                self.clients.append(client)
                self.broadcast(f"{nickname} joined the chat!".encode("utf-8"))
                client.send("Connected to the server!".encode("utf-8"))
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except ConnectionResetError:
                print("Connection reset by peer")
            except Exception as e:
                print(f"Error: {e}")

    def start(self):
        self.receive()

    
if __name__ == "__main__":
    try:
        server = Server()
        server.start()
    except KeyboardInterrupt:
        server.server.close()
        print("Cerrando...")
        logging.info("Server closed")
        logging.shutdown()
