import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_msg,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.load(payload)# decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return "Invalid response"
    
    def parse_error(self, payload):
        time = payload.get('timestamp')
        content = payload.get('content')
        return '[Error: ' + content + "," + time + ']'
    def parse_info(self, payload):
        time = payload.get('timestamp')
        content = payload.get('content')
        return '[Info: ' + content + "," + time + ']'
    def parse_msg(self, payload):
        time = payload.get('timestamp')
        content = payload.get('content')
        return '[Message: ' + content + "," + time + 'from: ' + payload.get('sender') + ']'
    def parse_history(self, payload):
        MessageHistory = payload.get('content')
        ParsedMsg = ''
        for msg in MessageHistory:
            ParsedMsg = ParsedMsg + self.parse_msg(json.load(msg)) + "\n"
        return ParsedMsg
                                                                            
    # Include more methods for handling the different responses... 
