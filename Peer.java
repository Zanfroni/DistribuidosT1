// Bibliotecas de estabelecimento de conexao do Java
import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;

public class Peer{
	
	// Peer tera seu IP
	private String ip;
	
	// Cria o Peer
	public Peer(String ip){
		this.ip = ip;
		start();
	}
	
	private String getIp(){
		return ip;
	}
	
	// Bases for new methods
	// Starts an user interface. If he get disconnected, comes back here
	private void start(){
	}
	
	// Logs on a Super Node
	private void login(){
	}
	
	// Thread that sends "Im here"
	private void stillAlive(){
	}
	
	// Requests a file from another Peer to the Supernode
	private void requestFile(){
	}
	
	// Receives response from SuperNode
	private void getRequest(){
	}
	
	// Listens to Supernode
	private void listen(){
	}
	
	// Send answer to Supernode
	private void answer(){
	}
	
	// Gets file from another node
	private void getFile(){
	}
	
	// Transmits file to another node
	private void transmitFile(){
	}
	
	// Logout from current supernode
	private void logout(){
	}
	
}
