'''
Based on stompy: https://bitbucket.org/benjaminws/python-stomp/
Created on 2015年1月9日
This file is to define the stomp protocol frame class.
A frame will be sent to server or received from server through connected network based on socket.

@author: Jidong
'''
import socket
import random
from queue import Queue

#hello='''MESSAGE\x0asubscription:0\x0amessage-id:007\x0adestination:/queue/a\x0acontent-type:text/plain\x0a\x0ahello queue a\x00'''

class Frame(object):
    '''
    classdocs
    '''

    def __init__(self, sock = None):
        '''
        Constructor
        '''
        self.framecmd = None
        self.frameheader = {}
        self.framebody = None
        self.sock = sock    #Assume we have connected the server
        try:
            self.myname=socket.gethostbyname(socket.gethostname())
            #print("host name: {0}".format(self.myname))
        except :
            print ("Error for gethostbyname()")
        #self.message = Queue()
        
    def build_frame(self, dict_args):
        '''build a frame based on a dict '''
        self.framecmd = dict_args.get('command')
        self.frameheader = dict_args.get('header')
        self.framebody = dict_args.get('body')
        return self
    
    def send_frame(self, frame_str):
        self.sock.sendall(frame_str)

    def frame_to_string(self):
        header = ("{0}:{1}\n".format(key, value) for key, value in self.frameheader.items())
        frame = "{0}\n{1}\n{2}".format(self.framecmd, "".join(header), self.framebody)
        return frame

    def receive_frame(self, nonblocking = False):
        singleframe = self._get_single_frame_from_socket()
        if not singleframe:
            return
        command = singleframe.split('\n', 1)[0]
        singleframe = singleframe[len(command)+1:]
        header, _, body = singleframe.partition("\n\n")
        if not header:
            print("There is not a header in the frame")
        #here is maybe some problems. About the order
        header = self.parse_header_to_dict(header)
        return self.build_frame({'command': command,
                                 'header': header,
                                 'body': body})
            
    def parse_header_to_dict(self, header_str):
        '''
        The single statement in this function comprehends these as following:
        >>> header_str = 'subscription:0\nmessage-id:007\ndestination:/queue/a\ncontent-type:text/plain'
        >>> header_list = header_str.split('\n')
        ['subscription:0', 'message-id:007', 'destination:/queue/a', 'content-type:text/plain']
        >>> dict(hline.split(':') for hline in header_list)
        {'subscription': '0', 'destination': '/queue/a', 'content-type': 'text/plain', 'message-id': '007'}
        In other words, dict() funcion must be used as iterable expression, for example:
        >>> header = ['subscription:0']
        we can use "dict(i.split(':') for i in header)" to change the list to dict: {'subscription': '0'}
        whereas we can't use "dict(header[0].split(':'))", neither can "dict(['subscription', '0'])"
        '''
        return dict(hline.split(":",1) for hline in header_str.split('\n'))
        
    
    def _get_single_frame_from_socket(self):
        try:
            buffer=""
            pbyte=""
            while not buffer.endswith('\x00'):
                try:
                    #get a single byte from socket
                    pbyte = self.sock.recv(1)
                    if not pbyte or pbyte == "":
                        print ("Nothing in sock")
                except:
                    raise RuntimeError("Error in Socket")
                buffer = buffer + pbyte.decode("utf-8")
        finally:
            foo=1
        if buffer[:1]=='\n':
            #We need to remove the '\n', which is striped from the previous frame.
            return buffer[1:-1]
        #The other kinds of frame:
        return buffer[:-1]
    
    
    '''
        frame='MESSAGE\x0asubscription:0\x0a\
message-id:007\x0a\
destination:/queue/a\x0a\
name:\x0a\
content-type:text/plain\x0a\x0a\
hello queue a\x00'
        print("received raw frame:")
        print(frame)
        return frame
    '''

    '''
    #just for experiment
    def _get_single_frame_from_socket(self):
        try:
            buffer=""
            pbyte=""
            try:
                #get a single byte from socket
                pbyte = self.sock.recv(6000)
                if not pbyte or pbyte == "":
                    print ("Nothing in sock")
            except:
                raise RuntimeError("Error in Socket")
            buffer = buffer + pbyte.decode("utf-8")
            print(len(buffer))
            print(buffer)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        finally:
            foo=1
        if buffer[:1]=='\n':
            return buffer[1:-1]
        return buffer[:-1]
    '''
    
    def print_frame(self):
        pass

if __name__ == '__main__':
    print ("test frame.py")
    hf = Frame()
    hf.receive_frame()
    print ("\nreceived frame:")
    print(hf.framecmd)
    print(hf.frameheader)
    print(hf.framebody)
    print("\n~~~~~~~~~~~~~~~~~~")
    framestr=hf.frame_to_string()
    print(framestr)
