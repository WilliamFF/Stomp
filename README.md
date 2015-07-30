# Stomp
STOMP protocol client, connecting to and communicating with Apache ActiveMQ.

Based on stompy: http://bitbucket.org/benjaminws/python-stomp/. 

I simplified it. :)

How to use:

Input stomp.py and frame.py into your project folder and 

>> from stomp import Stomp
>> stomp = Stomp(serveraddr="127.0.0.1")
>> stomp.connect_server()
>> stomp.send(destination="/queue/test", body="Hello!")
>> stomp.dis_connect_server()
>> 
>> receiver = Stomp(serveraddr="127.0.0.1")
>> receiver.connect_server()
>> receiver.subscribe(destination="/queue/test", id="receiver")
>> receiver.receive()
>> print (receiver.frame.framebody)
>> Hello!
>> receiver.unsubscribe(id="receiver")
>> receiver.dis_connect_server()