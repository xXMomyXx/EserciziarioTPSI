import socket
import threading

NDISPONIBILITA = 3

# Definizione variabili globali affinché siano comuni a tutti i client
disponibilita = NDISPONIBILITA
shutdown = False
# lock: variabile che usata con 'with' prima di un blocco di codice permette l'accesso a questo soltanto a un thread alla volta,
# evitando accessi concorrenti a una variabile (in questo caso a disponibilita)
lock = threading.Lock()


def centralInstance(conn, addr):
    # Dichiarazione riferimento a variabile globale
    global disponibilita, shutdown
    print(f"Connessione stabilita con {addr}")
    # Loop che riceve la richiesta dell'utente e risponde
    while True:
        # Ricezione città di partenza e arrivo dall'utente come unica stringa
        data = conn.recv(1024).decode()
        # Controllo che la stringa recepita contenga qualcosa, sennò esco dal loop
        if not data:
            break
        # Assegnazione città di partenza e arrivo alle variabili corrispondenti dividendo la stringa data in 2 nel punto
        # in cui è presente '|'
        partenza, arrivo = data.split("|")
        # Si pone il codice nel blocco sotto a 'with lock' per il motivo spiegato nel commento a riga 9
        with lock:
            if disponibilita == 0:
                response = 'Non ci sono più taxi disponibili. Server in chiusura.'
                conn.send(response.encode())
                shutdown = True
                break
            # Ci sono taxi disponibili: Invio risposta e riduzione di 1 dei taxi disponibili
            elif disponibilita > 0:
                # Possibili risposte:
                # Non ci sono taxi disponibili: Invio risposta e uscita dal loop;
                response = f"Taxi da {partenza} ad {arrivo} assegnato"
                disponibilita -= 1
                # Invio risposta come sequenza di byte (encode()) al client
                conn.send(response.encode())
    # Chiusura connessione con client e chiusura server se finiscono i taxi disponibili
    conn.close()
    print(f"Connessione terminata con {addr}")


def start_server():
    global shutdown
    # Inizializzazione lato server della socket su porta 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    # settimeout(1): Attende per massimo 1 secondo una connessione, altrimenti solleva un'eccezione. Facciamo questo poiché
    # il codice a riga 60 è bloccante, e senza un controllo continuo ogni secondo il loop del server dovrà fare un'iterazione in più
    # prima di rendersi conto che 'shutdown = True' e uscire
    server_socket.settimeout(1)
    print("Server in ascolto sulla porta 12345...")
    # Loop che accetta continuamente le nuove connessioni
    while not shutdown:
        # Try catch per controllare se si è connesso un client, altrimenti se non si connette e si solleva un
        # eccezione (per via di settimeout(1)) si passa alla prossima iterazione
        try:
            conn, addr = server_socket.accept()
            '''Inizializzazione thread(Processo a sè stante che esegue
               la funzione di gioco per l'istanza corrente)'''
            threading.Thread(
                # target: Funzione che il thread eseguirà
                target=centralInstance,
                # args: Argomenti che verranno passati alla funzione passata come target
                args=(conn, addr)
            ).start()  # Avvio del thread
        except socket.timeout:
            continue
    # Terminato il loop il server viene chiuso
    server_socket.close()


# Chiamata della funzione 'start_server' in main
if __name__ == "__main__":
    start_server()
