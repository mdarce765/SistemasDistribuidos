import zmq
import msgpack

ctx = zmq.Context()
servRep = ctx.socket(zmq.REP)
servPull= ctx.socket(zmq.PULL)
servPush = ctx.socket(zmq.PUSH)
servRep.bind("tcp://*:5555")
servPull.bind("tcp://*:5556")

time = 0
##ctx = zmq.Context.instance()
##pub.connect("tcp://localhost:5555")
##Pub = 
##Sub
while True:
    resp = servPull.recv_string()
    print(resp)
    
