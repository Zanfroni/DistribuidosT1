// Bibliotecas nativas do Java
import java.io.IOException;

// Classe que o usuario executa pra iniciar o programa
public class App{
	
	public static void main(String[] args) throws IOException {
		
		// Limpa a tela para evitar poluicao para o usuario
		clear();
		
		// Verifica entrada do usuario para definir se e Super nodo ou Peer
		// Exemplo de entrada: java App peer 127.0.0.1
		try{
			String type = args[0];
			if(type.equals("supernode")){
				new Supernode(args[1]);
			} else if(type.equals("peer")) {
				new Peer(args[1]);
			} else {
				System.out.println("Invalid input. Please try again\n");
				System.out.println("First argument must be either peer or supernode.");
				System.out.println("Second argument must be the PC's IP.");
			}
		} catch(Exception e){
			System.out.println("Fatal error while reading your input!");
			System.out.println("Please try again!");
		}
	}
	
	// Metodo que limpa a tela do terminal
	private static void clear(){
		System.out.print("\033[H\033[2J");  
		System.out.flush(); 
	}
	
}
