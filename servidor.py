import zmq
import msgpack
import time
import sqlite3
ctx = zmq.Context()
poller = zmq.Poller()
servEnd = "tcp://localhost:5556"
servRep = ctx.socket(zmq.REP)
servPull= ctx.socket(zmq.PULL)
servPush = ctx.socket(zmq.PUSH)
servRep.bind("tcp://*:5555")
servPull.bind("tcp://*:5556")
poller.register(servRep,zmq.POLLIN)
poller.register(servPull,zmq.POLLIN)

horarioLocal = 0
BD = sqlite3.connect("chats.db")

class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
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
        print(msg.conteudoRecv)
        
        servPush.connect(msg.end) ##conecta ao cliente
        servPush.send_string("ola :)")
        print(f"mensagem mandada para {msg.end}")
        servPush.disconnect(msg.end) ##disconecta do cliente
        
    if portas.get(servRep) == zmq.POLLIN:
        recv = servRep.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
        print(msg.conteudoRecv)
        if msg.tipoRecv == "reqChat":
            resp = "Usr1: msg1\nUsr2: msg2\n" ##eventualmente conectar a banco de dados sqlite
            servRep.send_string(f"{servEnd},{horarioLocal},repChat,{resp}")
        else:
            resp = msg.conteudoRecv + "2"
            servRep.send_string(f"{servEnd},{horarioLocal},rep,{resp}")
    
        
    
