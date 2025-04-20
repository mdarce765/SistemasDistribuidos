import zmq
import msgpack
ctx = zmq.Context()
clientReq= ctx.socket(zmq.REQ)
clientPull= ctx.socket(zmq.PULL)
clientPush = ctx.socket(zmq.PUSH)
clientEnd = "tcp://*:5600" ##endereco do cliente
clientReq.connect("tcp://localhost:5555") ##endereco do Rep do load balancer (por agora serv)
clientPull.bind(clientEnd) ##endereco do pull do cliente
clientPush.connect("tcp://localhost:5556") #endereco do Pull do load balancer (por agora serv)
#estrutura da mensagem (ip de quem mandou,horarioLocal,tipo,conteudo)
horarioLocal = 1
while True:
    esc = int(input("Push(0) ou RepReq (1)? "))
    mensagem = input("Mensagem a ser mandada: ")
    if esc == 0:
       
        clientPush.send_string(f"{clientEnd},{horarioLocal},post,{mensagem}")
    elif esc == 1:
        
        clientReq.send_string(f"{clientEnd},{horarioLocal},req,{mensagem}")
        recv = clientReq.recv_string()
        print(recv)
    horarioLocal +=1



