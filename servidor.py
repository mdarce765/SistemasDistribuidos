import zmq

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
# BD = sqlite3.connect("chats.db")
# cursor = BD.cursor()
# cursor.execute("CREATE TABLE nic_nic2(user, msg)") ## Teste do DB
chat = "" ##eventualmente conectar a banco de dados sqlite
posts = "" ##eventualmente conectar a banco de dados sqlite

class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
        
        if self.tipoRecv == "msg": ## (end,time,tipo,tituloConversa,usuario,conteudo)
            self.conversa = conteudo[3] ##conversa atual / chat table
            self.usuario = conteudo[4] ## quem enviou
            self.conteudoMsg = conteudo[5] ## mensagem enviada
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
    time.sleep(0.5)
    portas = dict(poller.poll())
    
    if portas.get(servPull) == zmq.POLLIN: ## chat!
        
        recv = servPull.recv_string()
        msg = mensagem(recv)
        print(f"PUSH recebido\n {recv}")
        conferirHorario(msg.horarioRecv)
        # exist = cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{msg.conversa}'")
        # if exist.fetchone() == None:
            # cursor.execute(f"CREATE TABLE {msg.conversa}(conversa, user, msg)")
        # msg_history = cursor.execute(f"SELECT * FROM {msg.conversa}")
        # chat = msg_history.fetchall()
       
        if msg.tipoRecv == "msg":
            # print(f'msg {msg.usuario}')
            # print(f'content {msg.conteudoMsg}')
            # print(f"pre chat {msg.usuario}: {msg.conteudoMsg}")
            # chat += f"{msg.usuario}: {msg.conteudoMsg}\n" ##adiciona ao historico

            # chat.append(f"({msg.usuario}: {msg.conteudoMsg})") ##adiciona ao historico
            # print(type(chat))
            BD = sqlite3.connect("chats.db")
            cursor = BD.cursor()
            cursor.execute(f"""INSERT INTO {msg.conversa} VALUES
                           ('{msg.conversa}', '{msg.usuario}', '{msg.usuario}: {msg.conteudoMsg}')""")
            BD.commit()
            cursor.execute(f"SELECT conteudo FROM {msg.conversa}")
            chat = cursor.fetchall()
            BD.close()
            
            # Transformando a lista de tuplas em uma lista simples
            lista_simples = [item[0] for item in chat]
            # print(f'list= {lista_simples}')

            ## mandar o novo historico para os usuarios
            # cursor.execute(f"CREATE TABLE IF NOT EXISTS {msg.conversa}({msg.conversa} TEXT, {msg.usuario} TEXT, {msg.conteudoMsg} TEXT)")
            # novo_hist = ""
            # cursor.execute(f"SELECT user, conteudo FROM {msg.conversa}")
            # for row in cursor.execute(f"SELECT user, conteudo FROM {msg.conversa}"):
            #     novo_hist = 

            servPub.send_string(f"{msg.conversa}\n{chat}") ##Pub manda o novo historico para todos conectados
            # servPub.send_string(f"{chat}") ##Pub manda o novo historico para todos conectados
            print(f'msg {chat}')

        elif msg.tipoRecv == "seguir":
            ##adicionar o usuario a seguir a lista de usuarios que o usuario segue
            ## usuario = msg.usuario
            ## usuarioASeguir = msg.usuarioASeguir
            print(msg.usuario,msg.usuarioASeguir)
            pass
        elif msg.tipoRecv == "post":
            print(msg.usuario,msg.conteudoMsg)
        else:
            
            #  print("Else do ##CHAT")
            print("TIPO PUSH DE TESTE/INVALIDO RECEBIDO")
        #servPush.connect(msg.end) ##conecta ao cliente
        #servPush.send_string("ola :)")
        #print(f"mensagem mandada para {msg.end}")
        #servPush.disconnect(msg.end) ##disconecta do cliente
        
    if portas.get(servRep) == zmq.POLLIN: 
        recv = servRep.recv_string()
        msg = mensagem(recv)
        conferirHorario(msg.horarioRecv)
        print(f"REQ RECEBIDA\n{recv}")
        print(msg.conteudoRecv)
        
        if msg.tipoRecv == "reqChat": ##retorna o historico inicial do chat!
            BD = sqlite3.connect("chats.db")
            cursor = BD.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {msg.conteudoRecv}({msg.conteudoRecv} TEXT, user TEXT, conteudo TEXT)")
            # BD.commit()
            ##linkar variavel chat ao resultado da query da conversa
            cursor.execute(f"SELECT conteudo FROM {msg.conteudoRecv}")
            chat = cursor.fetchall()
            BD.close()
            print(f'reqCHat:\n {chat}')
            # BD.commit()
            servRep.send_string(f"{servEnd},{horarioLocal},repChat,{chat}")
        elif msg.tipoRecv == "verPost":
            ##linkar variavel posts ao resultado da query dos posts
            servRep.send_string(f"{servEnd},{horarioLocal},repPost,{posts}")
        else: ##Req de teste
            print("TIPO REQ DE TESTE/DESCONHECIDO UTILIZADO")
            respteste = msg.conteudoRecv + "2"
            servRep.send_string(f"{servEnd},{horarioLocal},rep,{respteste}")
    
        
    
