import zmq
import msgpack
ctx = zmq.Context()
clientReq= ctx.socket(zmq.REQ)
clientPull= ctx.socket(zmq.PULL)
clientPush = ctx.socket(zmq.PUSH)
clientReq.connect("tcp://localhost:5555") ##endereco do Rep do load balancer (por agora serv)
clientPull.bind("tcp://*:5600") ##endereco do pull do cliente
clientPush.connect("tcp://localhost:5556") #endereco do Pull do load balancer (por agora serv)
while True:
    clientPush.send_string(f"batata")



