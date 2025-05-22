# Sistemas Distribuídos
Murilo Darce Borges Silva - 24.122.031-8  
Nicolas Costa Coppola de Moraes - 22.122.099-9  
Rodrigo Simões Ruy - 24.122.092-0  

# Afazeres
* O projeto deve ser desenvolvido usando qualquer biblioteca de comunicação (e.g., ZeroMQ, gRPC, OpenMPI) e com pelo menos 3 linguagens diferentes (e.g., Python, Java, C, C++, JavaScript ou TypeScript, Go, Rust, Zig, Elixir, Gleam, Erlang...);
* Os processos que postam e/ou enviam mensagens podem ser controlados pelos usuários, ou fazer postagens/troca de mensagens de forma automática; (Python, Java, C).
* O projeto deve executar pelo menos 3 servidores e 5 usuários para testar;
* Para garantir que a sincronização dos relógios está funcionando, os relógios de todos os processos podem sofrer alterações na atualização deles de forma aleatória, podendo ser adiantados ou atrasados em até 1 segundo.
* A documentação do projeto deve conter:
  * Descrição do padrão de mensagem utilizado em todas as partes do projeto.
  * Descrição dos dados enviados nas mensagens.
  * Diagrama mostrando a relação entre os serviços implementados.
 
  * O cliente tem que ter request e sistema de push e pull.
  * servidor push e pull reply,
 
  * Para publicar = push do usuário.
  * Para visualizar = request reply cliente-servidor.
  * Em qualquer push que tiver, tem que ter o timestamp atual de quando foi postado em todas as mensagens.
  * Portas 5555-5558 para Load Balancer, 5558-5599 para servidores
  
  * Linguagens:
    * Cliente: C/C++
    * Load Balancer: python/Elixir
    * Servidor: python

  * Tabelas:
    * Posts
      * Usuário que mandou
      * Horário 
      * Conteúdo postado
    * Chats
      * Usuário que mandou
      * Horário
      * Conteudo
    * Seguir (Tabela para correlacionar seguidor e seguido)
      * Seguido
      * Seguidor

  * Load Balancer:
    * Pull: 5555
    * Rep: 5556
    * Pub: 5557
    * Sub: 5558

  * Servidores:
    * Pull
    * Rep
    * Pub
    
 
  
Bibliotecas necessárias para rodar o cliente em C:  
Biblioteca CZMQ: https://github.com/zeromq/czmq   
Executável incluído na pasta Grupo64!

Bibliotecas necessárias para rodar o cliente em Java :  
Biblioteca JeroMQ: https://github.com/zeromq/jeromq  
pom.xml incluído na pasta Grupo64!  

Bibliotecas necessárias para rodar o cliente em Python:  
Biblioteca Pyzmq: https://github.com/zeromq/pyzmq  
