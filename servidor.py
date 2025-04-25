import zmq
import msgpack
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
resp = "" ##eventualmente conectar a banco de dados sqlite
class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
        
        if self.tipoRecv == "msg":
            self.conversa = conteudo[3] ##conversa da qual 
            self.usuario = conteudo[4]
            self.conteudoMsg = conteudo[5]
        else:
            self.conteudoRecv = conteudo[3] 
        

        

def conferirHorario(horarioRecv):
    global horarioLocal
    if horarioRecv > horarioLocal:
        horarioLocal = horarioRecv
        print("Horario corrigido!")
            
while True:
    time.sleep(1)
    portas = dict(poller.poll())
    
    if portas.get(servPull) == zmq.POLLIN:
        
        recv = servPull.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
       
        if msg.tipoRecv == "msg":
            resp += f"{msg.usuario}:{msg.conteudoMsg}\n" ##adiciona ao historico
            ##mandar o novo historico para os usuarios
            servPub.send_string(f"{msg.conversa}\n{resp}")
            print(resp)
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
        
        if msg.tipoRecv == "reqChat": ##retorna o historico do chat!
            servRep.send_string(f"{servEnd},{horarioLocal},repChat,{resp}")
        else: ##Req de teste
            resp = msg.conteudoRecv + "2"
            servRep.send_string(f"{servEnd},{horarioLocal},rep,{resp}")
    
        
    
