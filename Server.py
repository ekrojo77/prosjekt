# -*- coding: utf-8 -*-
import SocketServer
import json
import re
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = {}
usernames = []
MessageHistory = []
client = ''


PosResponses = "Possible responses this server handles are: login, logout, msg and names"


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """


    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.users = (self, '')
        self.username = None

        

        # Loop that listens for messages from the client
        global client
        global MessageHistory
        while True:
            received_string = self.connection.recv(4096).decode('utf-8')
            print received_string
            request = json.loads(received_string).get('request')
            received_content = json.loads(received_string).get('content')

            def response_(sender,response,content):
                response =  {'timestamp':time.strftime("%H:%M:%S"),
                         'sender':sender,
                         'response':response,
                         'content':content}
                self.connection.send(json.dumps(response).encode('utf-8'))
            def sendMessages(self, data):
                payload = json.dumps(data)
                for client in users.values():
                    client.send(payload)
                    
            if(request == "login"):
                if(client == ""):
                    if(received_content != ""):
                        if(re.match("^[A-Za-z0-9]+$",received_content)):
                            if(received_content not in users.values()):
                                client = received_content
                                users[self] = received_content
                                response_('Server','info','Successful login')
                                time.sleep(0.1)
                                response_('Server','history',MessageHistory)
                                usernames.append(received_content)
                            else:
                                response_('Server','error','Username already taken')
                        else:
                            response_('Server','error','Username can only be letters and numbers')
                    else:
                        response_('Server','error','No username')
                else:
                    response_('Server','error','Already logged in')
            elif(request == "help"):
                response_('Server','error',PosResponses)
            elif(request == "logout") | (request == "msg") | (request == "names"):
                if(client != ''):
                    if(request == "logout"):
                            del users[self]
                            usernames.remove(client)
                            client = ''
                            response_('Server','info','You have been logged out')
                    elif(request == "msg"):
                        response =  {'timestamp':time.strftime("%H:%M:%S"),
                                     'sender':users[self],
                                     'response':'msg',
                                     'content':received_content}
                        history = {'timestamp':time.strftime("%H:%M:%S"),
                                     'sender':users[self],
                                     'response':'history',
                                     'content':received_content}
                        MessageHistory.append(history)
                        for user in users:
                            user.request.send(json.dumps(response))

                    elif(request == "names"):
                        ClientList = ''
                        for user in usernames:
                            ClientList += user + ', '
                        response_(users[self], 'info', ClientList)

                else:
                    response_('Server','error','You are not logged in')

            else:
                response_('Server','error','Unknown problem, try help')
                
                    
                
            
            # TODO: Add handling of received payload from client


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
