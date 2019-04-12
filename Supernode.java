// Bibliotecas nativas do Java
import java.util.ArrayList;
import java.io.IOException;

// Bibliotecas de estabelecimento de conexao do Java
import java.net.Socket;
import java.net.ServerSocket;
import java.net.MulticastSocket;

public class Supernode {
	
	// Super nodo tera seu IP e lista de peers vinculados a ele
	private String ip;
	private ArrayList<Peer> Nodes;
	private MulticastSocket socket;
	
	// Cria o Super nodo
	public Supernode(String ip) throws IOException {
		this.ip = ip;
		this.Nodes = new ArrayList<>();
		socket = new MulticastSocket(6969);
	}
}
