import zmq
import msgpack
import time
ctx = zmq.Context()
poller = zmq.Poller()
servEnd = "tcp://*:5556"
servRep = ctx.socket(zmq.REP)
servPull= ctx.socket(zmq.PULL)
servPush = ctx.socket(zmq.PUSH)
servRep.bind("tcp://*:5555")
servPull.bind(servEnd)
poller.register(servRep,zmq.POLLIN)
poller.register(servPull,zmq.POLLIN)

horarioLocal = 0
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
    if portas.get(servRep) == zmq.POLLIN:
        recv = servRep.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
        print(msg.conteudoRecv)
        resp = msg.conteudoRecv + "2"
        servRep.send_string(f"{servEnd},{horarioLocal},rep,{resp}")
    
        
    
