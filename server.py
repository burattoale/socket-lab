#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class ChatServer:
    """Multithreaded chat server."""
    
    def __init__(self, host='', port=33000):
        self.host = host
        self.port = port
        self.BUFSIZ = 1024
        self.clients = {}
        self.addresses = {}
        
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server started on port {self.port}")
        print("Waiting for connection...")
        print("Press Ctrl+C to stop the server.")
    
    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            try:
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
            name = client.recv(self.BUFSIZ).decode("utf8")
            welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
            client.send(bytes(welcome, "utf8"))
            msg = "%s has joined the chat!" % name
            self.broadcast(bytes(msg, "utf8"))
            self.clients[client] = name
    
            while True:
                msg = client.recv(self.BUFSIZ)
                if not msg:  # Empty message means client disconnected
                    break
                if msg != bytes("{quit}", "utf8"):
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
        accept_thread = Thread(target=self.accept_incoming_connections)
        accept_thread.start()
        try:
            accept_thread.join()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.server.close()
            print("Server closed.")


if __name__ == "__main__":
    server = ChatServer(host='', port=33000)
    server.run()