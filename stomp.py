'''
Based on stompy: https://bitbucket.org/benjaminws/python-stomp/
Created on Jan.12.2015
Modified on Mar.10.2015
This file is to implement stomp messaging protocol.The stomp protocol is easily
written. It is designed to be as simple as possible.
@author: Jidong
'''

import socket
from frame import Frame
import time

class Stomp(object):
    '''
    classdocs
    '''

    def __init__(self, serveraddr='172.18.15.26', port = 61613):
        '''
        Constructor
        '''
        self.serveraddr = serveraddr
        self.serverport = port
        self.servername = 'apachemq'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isconnected = False
        self.issubscribed = None
        self.accept_version = '1.1'
        self.subscribe_destination = '/queue/stomp'
        self.ack = 'auto'
        self.frame = Frame(self.sock)

        
    def connect_server(self, username=None, passcode=None):
        '''
        connect to stomp server
        '''
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        try:
            self.sock.connect((self.serveraddr, self.serverport))
        except ConnectionRefusedError:
            print("socket timeout")
            self.isconnected = False
            return self.isconnected
        headers = {}#????
        if username and passcode:
            self.frame.frameheader.update({'login':username, 'passcode':passcode})
        self.frame.frameheader.update({'accept-version':self.accept_version,})
        self.frame = self.frame.build_frame({'command':'CONNECT',\
                                           'header':self.frame.frameheader,\
                                           'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))
        self.frame.receive_frame()
        self.isconnected = True
        #print ("Connect activemq:")
        #print (self.frame.frameheader)
        return self.isconnected
            
    def dis_connect_server(self):
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        if self.issubscribed:
            self.unsubscribe()
        self.frame = self.frame.build_frame({'command':'DISCONNECT',\
                                             'header':self.frame.frameheader,\
                                             'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))
        self.sock.close()
        self.isconnected = False
    
    def send(self, destination="/queue/stomp", body="", content_type="text/plain", receipt=None):
        '''
        if the send frame has a receipt header, the server must reply a RECEIPT frame after successfuly deal with it.
        '''
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        self.frame.frameheader.update({'destination':destination, 'content-type':content_type})
        if receipt:
            self.frame.frameheader.update({'receipt':receipt})
        self.frame.frameheader.update({'content-length':len(body)})
        self.frame = self.frame.build_frame({'command':'SEND',\
                                             'header':self.frame.frameheader,\
                                             'body':body+'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))

    def receive(self):
        self.frame.receive_frame()
    
    def subscribe(self, id='0', destination="/queue/stomp", ack="auto"):
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        self.subscribe_destination = destination
        self.ack = ack
        self.frame.frameheader.update({'id':id})
        self.frame.frameheader.update({'destination':self.subscribe_destination, 'ack':self.ack})
        self.frame = self.frame.build_frame({'command':'SUBSCRIBE',\
                                             'header':self.frame.frameheader,\
                                             'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))
        self.issubscribed = True

    def unsubscribe(self, id='0'):
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        self.frame.frameheader.update({'id':id})
        self.frame = self.frame.build_frame({'command':'UNSUBSCRIBE',\
                                             'header':self.frame.frameheader,\
                                             'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))
        self.issubscribed = False

    def message_ack(self, id='0'):
        '''
        ack frame needs to include subscription id and message-id, transaction is optional.
        1. subscription id is to identify the consumer which are acknowledging the message.
        this must match the parament in subscribe().
        2. the message-id means which message are acknowledging by the consumer.
        this must match the value in received MESSAGE frame header from server, which identify each
        unique message.
        for example: 
        '''
        try:
            message_id = self.frame.frameheader['message-id']
        except KeyError:
            print("There is no message_id in the MESSAGE frame")
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        self.frame.frameheader.update({'subscription':id})
        self.frame.frameheader.update({'message-id':message_id})
        self.frame = self.frame.build_frame({'command':'ACK',\
                                             'header':self.frame.frameheader,\
                                             'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))

    def message_nack(self, id='0'):
        try:
            message_id = self.frame.frameheader['message-id']
        except KeyError:
            print("There is no message_id in the MESSAGE frame")
        self.frame.framecmd = None
        self.frame.frameheader = {}
        self.frame.framebody = None
        self.frame.frameheader.update({'subscription':id})
        self.frame.frameheader.update({'message-id':message_id})
        self.frame = self.frame.build_frame({'command':'NACK',\
                                             'header':self.frame.frameheader,\
                                             'body':'\x00'})
        self.frame.send_frame((self.frame.frame_to_string()).encode("utf-8"))

if __name__ == '__main__':
    stomp = Stomp()
    if not stomp.connect_server():
        print("connect failed")
    else:
        '''
        stomp1 = Stomp()
        stomp1.connect_server()
        stomp1.subscribe(destination="/queue/test", id="stomp1")
        
        stomp2 = Stomp()
        stomp2.connect_server()
        stomp2.subscribe(destination="/queue/test", id="stomp2")
        '''
        #fileHandle = open ( 'aaa.txt', encoding='utf-8')
        #body = fileHandle.read()
        body = 'hello stomp'
        for i in range(1, 500):
            stomp.send(destination="/queue/test", body=body+str(i), receipt=str(i))
            stomp.receive()
            print (stomp.frame.framecmd)
            print (stomp.frame.frameheader)
            print (stomp.frame.framebody)
            #time.sleep(0.02)
        #fileHandle.close()
        stomp.dis_connect_server()
        '''
        for i in range(1, 3):
            print("stomp1 receive:")
            stomp1.receive()
            print (stomp1.frame.framebody)
            #stomp2.message_ack(id="stomp1")
            
        for i in range(1, 3):
            stomp2.receive()
            print("stomp2 receive:")
            print (stomp2.frame.framebody)
            
        stomp1.unsubscribe(id="stomp1")
        stomp1.dis_connect_server()
        
        stomp2.unsubscribe(id="stomp2")
        stomp2.dis_connect_server()
        '''
    
