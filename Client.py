# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.receiver = MessageReceiver(self,self.connection)
        self.MessagePars = MessageParser()


        
        while True:
            input_ = raw_input().split(' ')
            if len(input_) != 0:
                if(input_[0] == "login"):
                    self.send_payload({'request': 'login', 'content': input_[1]})
                elif(input_[0] == "logout"):
                    self.send_payload({'request': 'logout',})
                elif(input_[0] == "msg"):
                    self.send_payload({'request': 'msg', 'content': input_[1]})
                elif(input_[0] == "names"):
                    self.send_payload({'request': 'names'})
                elif(input_[0] == "help"):
                    self.send_payload({'request': 'help'})
                else:
                    print "Error, type 'help'"
                
     
    def disconnect(self):
        self.connection.close()
        

    def receive_message(self, message):
        message = self.MessagePars.parse(message)
        print message
        

    def send_payload(self, data): 
        payload = json.dumps(data).encode("utf-8")
        self.connection.send(payload)
        
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)

