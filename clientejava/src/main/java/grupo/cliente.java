package grupo;
import org.zeromq.SocketType;
import org.zeromq.ZMQ;
import org.zeromq.ZContext;
import org.zeromq.ZMQ.Socket;
import java.util.Scanner;  

public class cliente
{
    public static void main(String[] args) throws Exception
    {
        try (ZContext context = new ZContext()) {
            // Socket to talk to clients
            Scanner myObj = new Scanner(System.in);  
            Socket clientPush = context.createSocket(SocketType.PUSH);
            Socket clientReq = context.createSocket(SocketType.REQ);
            Socket clientSub = context.createSocket(SocketType.SUB);
            clientReq.connect("tcp://localhost:5555");
            clientPush.connect("tcp://localhost:5556");
            clientSub.connect("tcp://localhost:5557");

            
            
            System.out.println("TESTOU!");
            clientPush.send("End,1234,Tipo,Conteudo".getBytes(ZMQ.CHARSET),0);
            clientReq.send("End,1234,Tipo,Conteudo".getBytes(ZMQ.CHARSET),0);
            String resp = clientReq.recvStr();
            System.out.println(resp);
            Thread.sleep(5000); //precisa de wait, pqp que bosta :(
            
        }
    }
}