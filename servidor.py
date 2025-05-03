import zmq
## import msgpack
import time
import sqlite3
ctx = zmq.Context()
poller = zmq.Poller()
portaserv = 5556
servEnd = f"tcp://localhost:{portaserv}"
servPub = ctx.instance().socket(zmq.PUB)
servPub.bind("tcp://*:5557")
servRep = ctx.socket(zmq.REP)
servPull= ctx.socket(zmq.PULL)
servPush = ctx.socket(zmq.PUSH)
servRep.bind("tcp://*:5555")
servPull.bind(f"tcp://*:{portaserv}")

poller.register(servRep,zmq.POLLIN)
poller.register(servPull,zmq.POLLIN)
## (ip de quem mandou,horarioLocal,tipo,conteudo)
## 
## ... msg,"usr1-usr2 usr1 mensagem"
horarioLocal = 0
BD = sqlite3.connect("chats.db")
chat = "" ##eventualmente conectar a banco de dados sqlite
posts = "" ##eventualmente conectar a banco de dados sqlite
class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
        
        if self.tipoRecv == "msg": ## (end,time,tipo,tituloConversa,usuario,conteudo)
            self.conversa = conteudo[3] ##conversa atual
            self.usuario = conteudo[4]
            self.conteudoMsg = conteudo[5]
        elif self.tipoRecv == "post": ## (end,time,tipo,usuario,conteudo)
            self.usuario = conteudo[3]
            self.conteudoMsg = conteudo[4]
        elif self.tipoRecv == "seguir":
            self.usuario = conteudo[3]
            self.usuarioASeguir = conteudo[4]
        else: ## (end,time,tipo,conteudo)
            self.conteudoRecv = conteudo[3] 
        

        

def conferirHorario(horarioRecv):
    global horarioLocal
    if horarioRecv > horarioLocal:
        horarioLocal = horarioRecv
        print("Horario corrigido!")
            
while True:
    time.sleep(1)
    portas = dict(poller.poll())
    
    if portas.get(servPull) == zmq.POLLIN: ## chat!
        
        recv = servPull.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
       
        if msg.tipoRecv == "msg":
            chat += f"{msg.usuario}:{msg.conteudoMsg}\n" ##adiciona ao historico
            ##mandar o novo historico para os usuarios
            servPub.send_string(f"{msg.conversa}\n{chat}") ##Pub manda o novo historico para todos conectados
            print(chat)
        elif msg.tipoRecv == "seguir":
            ##adicionar o usuario a seguir a lista de usuarios que o usuario segue
            ## usuario = msg.usuario
            ## usuarioASeguir = msg.usuarioASeguir
            pass
        elif msg.tipoRecv == "post":
            print(msg)
        else:
            
             print(msg.conteudoRecv)
        #servPush.connect(msg.end) ##conecta ao cliente
        #servPush.send_string("ola :)")
        #print(f"mensagem mandada para {msg.end}")
        #servPush.disconnect(msg.end) ##disconecta do cliente
        
    if portas.get(servRep) == zmq.POLLIN: 
        recv = servRep.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
        print(msg.conteudoRecv)
        
        if msg.tipoRecv == "reqChat": ##retorna o historico inicial do chat!
            ##linkar variavel chat ao resultado da query da conversa
            servRep.send_string(f"{servEnd},{horarioLocal},repChat,{chat}")
        elif msg.tipoRecv == "verPost":
            ##linkar variavel posts ao resultado da query dos posts
            servRep.send_string(f"{servEnd},{horarioLocal},repPost,{posts}")
        else: ##Req de teste
            respteste = msg.conteudoRecv + "2"
            servRep.send_string(f"{servEnd},{horarioLocal},rep,{respteste}")
    
        
    
