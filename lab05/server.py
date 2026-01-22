#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class ChatServer:
    """Multithreaded chat server."""
    
    def __init__(self, host='', port=33000):
        self.host = host
        self.port = port
        self.BUFSIZ = 1024 # lunghezza del buffer in byte
        # TODO crea due dizionari vuoti, uno per i client e l'altro per gli indirizzi
        self.clients = 
        self.addresses = 
        
        # TODO crea un socket con parametri le costanti AF_INET e SOCK_STREAM
        # poi connettilo alla tupla (self.host, self.port)
        # suggerimento: sono due righe di codice: una per creare il socket, l'altra per il bind
        self.server = 

        self.server.listen(5)# permetti fino a 5 tentativi di connessione falliti
        print(f"Server started on port {self.port}")
        print("Waiting for connection...")
        print("Press Ctrl+C to stop the server.")
    
    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            try:
                # TODO usa il socket self.server per accettare la connessione del client
                client, client_address = self.server.accept()
                print("%s:%s has connected." % client_address)
                client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
                self.addresses[client] = client_address
                Thread(target=self.handle_client, args=(client,)).start()
            except OSError:
                break  # Server socket has been closed
    
    def handle_client(self, client):
        """Handles a single client connection."""
        
        name = None
        try:
            # TODO client e' un socket salva su name il messaggio di lunghezza self.BUFSIZ decodificato come "utf8"
            # che ricevi su questo socket
            name = 
            welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
            
            client.send(bytes(welcome, "utf8"))
            msg = "%s has joined the chat!" % name
            # TODO manda a TUTTI i client una notifica per avvertire del nuovo arrivo nella chat
            # suggerimento: usa il metodo broadcast di questa classe per mandare msg dopo aver usato il cast a bytes in "utf8"
            # con bytes(<stringa del messaggio>, <tipo di codifica>)
            # Il metodo self.broadcast ha la stessa sintassi del metodo send dei socket
            
            # TODO aggiungi il nome scelto dall'utente alla lista dei client
            self.clients[client] = 
    
            while True: # Loop principale
                msg = client.recv(self.BUFSIZ)
                if not msg:  # Empty message means client disconnected
                    break
                if msg != bytes("{quit}", "utf8"): # manda a tutti i client il messaggio
                    self.broadcast(msg, name+": ")
                else:
                    client.send(bytes("{quit}", "utf8"))
                    break
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError) as e:
            print(f"Connection error with {name if name else 'unknown client'}: {e}")
        finally:
            # Clean up the client connection
            if client in self.clients:
                del self.clients[client]
            if client in self.addresses:
                del self.addresses[client]
            try:
                client.close()
            except:
                pass
            if name:
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                print(f"{name} has disconnected.")
    
    def broadcast(self, msg, prefix=""):
        """Broadcasts a message to all the clients."""
        
        for sock in list(self.clients.keys()):
            try:
                sock.send(bytes(prefix, "utf8")+msg)
            except (OSError, BrokenPipeError):
                pass  # Client will be removed by handle_client
    
    def run(self):
        """Start the server and handle connections."""
        # TODO crea un thread che abbia come target la funzione self.accept_incoming_connections
        accept_thread = 
        accept_thread.start()
        try:
            accept_thread.join()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.server.close()
            print("Server closed.")


if __name__ == "__main__":
    # TODO crea un oggetto ChatServer con host='' e port=<valore che vuoi>
    # IMPORTANTE: ricordarsi il numero di porta e se modificato qui cambiare anche il default sul client
    # se in dubbio tenere 33000
    server = 
    server.run()