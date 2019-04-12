// Bibliotecas nativas do Java
import java.util.ArrayList;
import java.io.IOException;

// Bibliotecas de estabelecimento de conexao do Java
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.MulticastSocket;

public class Supernode {
	
	// Super nodo tera seu IP e lista de peers vinculados a ele
	private String ip;
	private ArrayList<Peer> Nodes;
	
	// Cria o Super nodo
	public Supernode(String ip) {
		this.ip = ip;
		this.Nodes = new ArrayList<>();
		start();
	}
	
	private String getIp(){
		return ip;
	}
	
	// Bases for new methods
	// Starts an user interface. If he get disconnected, comes back here
	private void start(){
	}
	
	// Log peer
	
	// Thread that receives the "Im here"
	private void getPeer(){
	}
	
	// Receive Multicast
	
	// Send back Multicast to supernode
	
	// Receive peer
	
	// Send Multicast
	
	// Get Response
	
	// Responds to Peer
	
	// Disable the entire system
	private void logout(){
	}
}
