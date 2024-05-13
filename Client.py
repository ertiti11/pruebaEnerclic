import socket
import threading

class Client:
    def __init__(self):
        self.ip = "172.17.0.2"
        self.port = 4444
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        self.nickname = input("Elige un apodo: ")

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message == "NICK":
                    self.client.send(self.nickname.encode("utf-8"))
                else:
                    print(message)
            except ConnectionResetError:
                print("La conexión ha sido interrumpida por el host remoto.")
                self.client.close()
                break
            except ConnectionAbortedError:
                print("La conexión ha sido interrumpida.")
                self.client.close()
                break
            except EOFError:
                print("Saliendo...")
                self.client.close()
                break
    
    def write(self):
        while True:
            try:
                message = f"{self.nickname}: {input('')}"
                self.client.send(message.encode("utf-8"))
            except:
                print("¡Ocurrió un error!")
                self.client.close()
                break
    
    def start(self):
        try:
            receive_thread = threading.Thread(target=self.receive, daemon=True)
            receive_thread.start()
            write_thread = threading.Thread(target=self.write, daemon=True)
            write_thread.start()
            receive_thread.join()
            write_thread.join()
        except KeyboardInterrupt:
            print("Cerrando...")
            self.client.close()
    
if __name__ == "__main__":
    try:
        client = Client()
        client.start()
    except KeyboardInterrupt:
        print("Cerrando...")