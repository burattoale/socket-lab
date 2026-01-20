"""Script for terminal-based chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class ChatClient:
    """Chat client application for terminal."""
    
    def __init__(self, host, port):
        self.BUFSIZ = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True
        
        # Start receive thread
        receive_thread = Thread(target=self.receive, daemon=True)
        receive_thread.start()
    
    def receive(self):
        """Handles receiving of messages."""
        while self.running:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                if not msg:
                    print("\n[Server disconnected]")
                    self.running = False
                    break
                print(f"\n{msg}")
                print("> ", end="", flush=True)
            except (OSError, ConnectionResetError, ConnectionAbortedError):
                if self.running:
                    print("\n[Connection lost]")
                    self.running = False
                break
    
    def send(self, msg):
        """Handles sending of messages."""
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.running = False
                self.client_socket.close()
                return False
            return True
        except (OSError, BrokenPipeError):
            print("[Connection error]")
            self.running = False
            return False
    
    def run(self):
        """Start the chat client."""
        print("Connected to server. Type '{quit}' to exit.")
        
        while self.running:
            try:
                print("> ", end="", flush=True)
                msg = input()
                if not self.send(msg):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n[Disconnecting...]")
                self.send("{quit}")
                break
        
        print("Goodbye!")


if __name__ == "__main__":
    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)
    
    client = ChatClient(HOST, PORT)
    client.run()