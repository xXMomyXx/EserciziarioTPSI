import socket
import threading

NDISPONIBILITA = 3

# Definizione variabile numero disponibilità come globale affinché sia comune a tutti i client
disponibilita = NDISPONIBILITA
shutdown = False


def centralInstance(conn, addr):
    # Dichiarazione riferimento a variabile globale
    global disponibilita, shutdown
    print(f"Connessione stabilita con {addr}")
    # Loop che riceve la richiesta dell'utente e risponde
    while True:
        # Ricezione città di partenza e arrivo dall'utente come unica stringa
        data = conn.recv(1024).decode()
        # Assegnazione città di partenza e arrivo alle variabili corrispondenti dividendo la stringa data in 2 nel punto
        # in cui è presente '|'
        partenza, arrivo = data.split("|")
        # Possibili risposte:
        # Non ci sono taxi disponibili: Invio risposta e uscita dal loop;
        if disponibilita == 0:
            response = 'Non ci sono più taxi disponibili. Server in chiusura.'
            conn.send(response.encode())
            shutdown = True
            break
        # Ci sono taxi disponibili: Invio risposta e riduzione di 1 dei taxi disponibili
        elif disponibilita > 0:
            response = f"Taxi da {partenza} ad {arrivo} assegnato"
            disponibilita -= 1
        # Invio risposta come sequenza di byte (encode()) al client
        conn.send(response.encode())
    # Chiusura connessione con client e chiusura server se finiscono i taxi disponibili
    conn.close()
    print(f"Connessione terminata con {addr}")


def start_server():
    global disponibilita
    # Inizializzazione lato server della socket su porta 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server in ascolto sulla porta 12345...")
    # Loop che accetta continuamente le nuove connessioni
    while not shutdown:
        conn, addr = server_socket.accept()
        '''Inizializzazione thread(Processo a sè stante che esegue
           la funzione di gioco per l'istanza corrente)'''
        client_thread = threading.Thread(
            # target: Funzione che il thread eseguirà
            target=centralInstance,
            # args: Argomenti che verranno passati alla funzione passata come target
            args=(conn, addr)
        ).start()  # Avvio del thread
    server_socket.close()


# Chiamata della funzione 'start_server' in main
if __name__ == "__main__":
    start_server()

# Da sistemare che il server ancora non si chiude e che soltanto il client che ha fatto l'ultima richiesta si chiude,
# non tutti
