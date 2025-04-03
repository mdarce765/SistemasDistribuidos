import zmq
import msgpack
ctx = zmq.Context()
clientReq= ctx.socket(zmq.REQ)
clientPull= ctx.socket(zmq.PULL)
clientPull.bind("tcp://*:5600") ##cliente
clientPush = ctx.socket(zmq.PUSH)
clientPush.connect("tcp://localhost:5555") #Load balancer



