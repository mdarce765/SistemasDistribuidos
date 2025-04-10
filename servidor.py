import zmq
import msgpack
import time
ctx = zmq.Context()
poller = zmq.Poller()
servRep = ctx.socket(zmq.REP)
servPull= ctx.socket(zmq.PULL)
servPush = ctx.socket(zmq.PUSH)
servRep.bind("tcp://*:5555")
servPull.bind("tcp://*:5556")
poller.register(servRep,zmq.POLLIN)
poller.register(servPull,zmq.POLLIN)

clock = 0
##ctx = zmq.Context.instance()
##pub.connect("tcp://localhost:5555")
##Pub = 
##Sub
while True:
    time.sleep(1)
    portas = dict(poller.poll())
    if portas.get(servPull) == zmq.POLLIN:
        
        recv = servPull.recv_string()
        print(recv)
    if portas.get(servRep) == zmq.POLLIN:
        recv = servRep.recv_string()
        print(recv)
        resp = recv + "2"
        servRep.send_string(resp)
        
    
