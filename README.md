###STOMP protocol client
#####connecting to and communicating with Apache ActiveMQ.

>Based on stompy: http://bitbucket.org/benjaminws/python-stomp/. I simplified it. :)

How to use:

Input stomp.py and frame.py into your project folder and:
```python
    >> from stomp import Stomp
    >>
    >> stomp = Stomp(serveraddr="127.0.0.1")
    >> stomp.connect_server()
    >> stomp.send(destination="/queue/test", body="Hello!")
    >> stomp.dis_connect_server()
    >> 
    >> stompreceiver = Stomp(serveraddr="127.0.0.1")
    >> stompreceiver.connect_server()
    >> stompreceiver.subscribe(destination="/queue/test", id="stompreceiver")
    >> stompreceiver.receive()
    >> print (stompreceiver.frame.framebody)
    >> Hello!
    >>
    >> stompreceiver.unsubscribe(id="stompreceiver")
    >> stompreceiver.dis_connect_server()
```
