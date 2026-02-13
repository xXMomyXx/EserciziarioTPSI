import socket
import json

# Variabili globali per memorizzare il film e il numero di biglietti richiesti dal client
selectedMovie = ""
selectedMovieBiglietti = 0

# Catalogo dei film: ogni voce contiene biglietti disponibili e prezzo unitario
movies = {
    "Il signore degli anelli": {
        "biglietti": 5,
        "prezzo": 6
    },
    "Oppenheimer": {
        "biglietti": 3,
        "prezzo": 8.5
    },
    "Interstellar": {
        "biglietti": 12,
        "prezzo": 9
    },
    "Il padrino": {
        "biglietti": 4,
        "prezzo": 7
    },
    "Avengers Endgame": {
        "biglietti": 5,
        "prezzo": 5
    }
}


def initServerSocket(address, port):
    """Crea e configura il socket del server, lo mette in ascolto sulla porta specificata."""
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((address, port))
    serverSocket.listen(5)
    print(f"Server in ascolto sulla porta {port}...")
    return serverSocket


def sendMoviesData(client, movies):
    """Invia al client il catalogo dei film in formato JSON."""
    data = json.dumps(movies)
    client.sendall(data.encode())


def receivePurchaseData(client):
    """Riceve dal client i dati di acquisto (film|quantità) e li salva nelle variabili globali."""
    global selectedMovie, selectedMovieBiglietti
    data = client.recv(1024).decode()
    selectedMovie, selectedMovieBiglietti = data.split("|")
    selectedMovieBiglietti = int(selectedMovieBiglietti)


def calculatePurchasePrice():
    """Calcola il prezzo totale in base alla quantità richiesta.
       Se la quantità supera la metà dei biglietti disponibili, applica uno sconto:
       un biglietto omaggio (sottrae il prezzo di un biglietto)."""
    scontoApplicato = False
    moviePrice = movies[selectedMovie]["prezzo"]
    bigliettiMovie = movies[selectedMovie]["biglietti"]

    if selectedMovieBiglietti > (bigliettiMovie / 2):
        scontoApplicato = True
        # Sconto: un biglietto gratis
        return (moviePrice * selectedMovieBiglietti) - moviePrice, scontoApplicato

    return moviePrice * selectedMovieBiglietti, scontoApplicato


def sendScontrino(client):
    """Invia al client il totale e l'indicazione se è stato applicato lo sconto."""
    purchaseValue, scontoApplicato = calculatePurchasePrice()
    if scontoApplicato:
        client.sendall(f"{purchaseValue}|True".encode())
    else:
        client.sendall(f"{purchaseValue}|False".encode())


if __name__ == '__main__':
    # Avvio del server su indirizzo locale porta 8080
    serverSocket = initServerSocket('127.0.0.1', 8080)

    while True:
        # Accetta una connessione in entrata
        conn, addr = serverSocket.accept()
        print(f'Connessione stabilita con: {addr}')

        # Fasi della comunicazione con il client:
        # 1. invio catalogo film
        sendMoviesData(conn, movies)
        # 2. ricezione richiesta di acquisto
        receivePurchaseData(conn)
        # 3. calcolo e invio dello scontrino
        sendScontrino(conn)

        # La connessione non viene chiusa esplicitamente;
        # il client terminerà la comunicazione.
        # conn.close()  # (commentata per mantenere aperta la connessione)
