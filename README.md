# Sistemas Distribuidos
Murilo Darce Borges Silva - 24.122.031-8  
Nicolas Costa Coppola de Moraes - 22.122.099-9  
Rodrigo Ruy Simões - 24.122.092-0  

# Afazeres
* O projeto deve ser desenvolvido usando qualquer biblioteca de comunicação (e.g., ZeroMQ, gRPC, OpenMPI) e com pelo menos 3 linguagens diferentes (e.g., Python, Java, C, C++, JavaScript ou TypeScript, Go, Rust, Zig, Elixir, Gleam, Erlang...);
* Os processos que postam e/ou enviam mensagens podem ser controlados pelos usuários ou fazer postagens/troca de mensagens de forma automática; (Python, Java, C)
* O projeto deve executar pelo menos 3 servidores e 5 usuários para testar;
* Para garantir que a sincronização dos relógios está funcionando, os relógios de todos os processos podem sofrer alterações na atualização deles de forma aleatória podendo ser adiantados ou atrasados em até 1 segundo;
* A documentação do projeto deve conter:
  * Descrição do padrão de mensagem utilizado em todas as partes do projeto
  * Descrição dos dados enviados nas mensagens
  * Diagrama mostrando a relação entre os serviços implementados
 
  * cliente tem que ter request e sistema de push e pull
  * servidor push e pull reply,
 
  * para pblicar = push do usuário
  * para visualizar = reqest reply cliente-servidor
  * em qlqr push que tiver, tem que ter o timestamp atual de quando foi postado em todas as mensagens
  * Todos os pulls tem que ter o "remetente"
 
Biblioteca ZMQ: https://zeromq.org/
