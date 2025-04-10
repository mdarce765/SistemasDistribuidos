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
    esc = int(input("Push(0) ou RepReq (1)? "))
    if esc == 0:
        clientPush.send_string(f"batata")
    elif esc == 1:
        clientReq.send_string(f"caraca!")
        recv = clientReq.recv_string()
        print(recv)



