"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


class ChatClient:
    """Chat client application with GUI."""
    
    def __init__(self, host, port):
        self.BUFSIZ = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, port))
        
        # Create GUI
        self.top = tkinter.Tk()
        self.top.title("Chatter")
        
        messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()
        self.my_msg.set("Type your messages here.")
        scrollbar = tkinter.Scrollbar(messages_frame)
        
        self.msg_list = tkinter.Listbox(messages_frame, height=15, width=50, 
                                         yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        messages_frame.pack()
        
        entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        send_button = tkinter.Button(self.top, text="Send", command=self.send)
        send_button.pack()
        
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start receive thread
        receive_thread = Thread(target=self.receive, daemon=True)
        receive_thread.start()
    
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                if not msg:
                    break
                self.msg_list.insert(tkinter.END, msg)
            except (OSError, ConnectionResetError, ConnectionAbortedError):
                break
            except RuntimeError:
                break
    
    def send(self, event=None):
        """Handles sending of messages."""
        msg = self.my_msg.get()
        self.my_msg.set("")
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
                self.top.quit()
        except (OSError, BrokenPipeError):
            self.top.quit()
    
    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send()
    
    def run(self):
        """Start the GUI main loop."""
        tkinter.mainloop()


if __name__ == "__main__":
    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)
    
    client = ChatClient(HOST, PORT)
    client.run()