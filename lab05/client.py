"""Script for terminal-based chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class ChatClient:
    """Chat client application for terminal."""
    
    def __init__(self, host, port):
        self.BUFSIZ = 1024 # number of bytes of the possible message

        # TODO crea un socket con parametri le costanti AF_INET e SOCK_STREAM
        # poi connettilo alla tupla (host, port)
        # suggerimento: sono due righe di codice: una per creare il socket, l'altra per il bind
        self.client_socket =

        self.running = True
        
        # TODO Crea un thread di ricezione che abbia come target la funzione self.receive
        # e che abbia l'opzione daemon settata a True
        # una volta creato fallo partire con start()
        receive_thread =
        
    
    def receive(self):
        """Handles receiving of messages."""
        while self.running:
            try:
                msg = # TODO ricevi dal socket un messaggio lungo self.BUFSIZ e decodificalo come sequenza di caratteri "utf8"
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
            # TODO manda il messaggio msg tramite self.client_socket come una sequenza di byte
            # codificati come "utf8"
            # suggerimento: fai il cast del messaggio con bytes(<stringa del messaggio>, <tipo di codifica>)
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

    # TODO Chiedi all'utente di inserire indirizzo IP e numero di porta su due righe differenti
    # suggerimento: usa input(<messaggio da mostrare all'utente>)
    # ricorda che quello che inserisci tra le parentesi di input() deve essere tra virgolette " "
    # perche' e' una stringa
    HOST = 
    PORT = 
    if not PORT: # indirizzo porta di default
        PORT = 33000
    else:
        PORT = int(PORT)
    
    # crea l'oggetto di ChatClient
    client = ChatClient(HOST, PORT)
    client.run()