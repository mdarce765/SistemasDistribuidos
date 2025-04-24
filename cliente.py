import zmq
import msgpack
ctx = zmq.Context()
clientReq= ctx.socket(zmq.REQ)
clientPull= ctx.socket(zmq.PULL)
clientPush = ctx.socket(zmq.PUSH)
portacliente = 5600
##clientEnd = f"tcp://localhost:{portacliente}" ##endereco do cliente
clientReq.connect("tcp://localhost:5555") ##endereco do Rep do load balancer (por agora serv)
## clientPull.bind(f"tcp://*:{portacliente}") ##endereco do pull do cliente
clientPush.connect("tcp://localhost:5556") #endereco do Pull do load balancer (por agora serv)
#estrutura da mensagem (ip de quem mandou,horarioLocal,tipo,conteudo)
horarioLocal = 1
while(True):
    try:
        clientPull.bind(f"tcp://*:{portacliente}")
        clientEnd = f"tcp://localhost:{portacliente}" ##endereco do cliente
        print(f"Bind na porta {portacliente}")
        break
    except:
        if (portacliente < 6000):
            portacliente += 1
        else:
            raise("FUDEU! Porta muito alta >= 6000!")
        
class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
        self.conteudoRecv = conteudo[3] 
        
        
while True:
    esc = int(input("Push(0) ou RepReq (1) ou Chat(2)? "))
    
    
    if esc == 0:
        mensagem = input("Mensagem a ser mandada: ")
        clientPush.send_string(f"{clientEnd},{horarioLocal},post,{mensagem}")
        recv = clientPull.recv_string()
        print(recv)
    elif esc == 1:
        mensagem = input("Mensagem a ser mandada: ")
        clientReq.send_string(f"{clientEnd},{horarioLocal},req,{mensagem}")
        recv = clientReq.recv_string()
        print(recv)
    elif esc == 2:
        usuario = input("Insira o seu usuario: ")
        usuarioEsc = input("Insira usuario com o qual quer conversar: ")
       
        alfabet = sorted([usuario,usuarioEsc])
        clientReq.send_string(f"{clientEnd},{horarioLocal},reqChat,{alfabet[0]}-{alfabet[1]}")
        recv = clientReq.recv_string()
        msg = mensagem(recv)
        
        print(msg.conteudoRecv)
        
    horarioLocal +=1
    



