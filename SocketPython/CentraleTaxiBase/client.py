import socket


def start_client():
    # Inizializzazione lato client della socket su porta 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Loop di inserimento per mandare richieste al server
    while True:
        print("-----CENTRALE TAXI------\n")
        # Inserimento città di partenza e di arrivo
        partenza = input("Inserire la città di partenza\n")
        arrivo = input("Inserire la città di arrivo\n")
        if partenza.isdigit() or arrivo.isdigit():
            print("Inserimento invalido. Reinserire")
            continue
        # Unione di città di partenza e arrivo in un unica stringa separate da '|'
        message = f"{partenza}|{arrivo}"
        # Invio della stringa sotto forma di sequenza di byte (encode())
        client_socket.sendall(message.encode())
        # Ricezione risposta server e decodifica della sequenza di byte (decode())
        response = client_socket.recv(1024).decode()
        # Presentazione su schermo della risposta ricevuta
        print(response)
        # Finita la disponibilità di taxi si esce dal loop
        if response == 'Non ci sono più taxi disponibili. Server in chiusura.':
            break
    # Finito il loop si chiude il lato client della socket
    client_socket.close()


# Chiamata della funzione 'start_client' in main
if __name__ == "__main__":
    start_client()
