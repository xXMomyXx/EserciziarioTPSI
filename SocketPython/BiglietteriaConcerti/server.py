import socket
import json

selectedConcerto = ""
selectedConcertoBiglietti = 0

concerti = {
    "Scorpion": {
        "nomeArtista": "Drake",
        "data": "20/11/2026",
        "prezzoBiglietto": 30,
        "postiDisponibili": 5
    },
    "Whole Lotta Red": {
        "nomeArtista": "Playboi Carti",
        "data": "04/05/2026",
        "prezzoBiglietto": 150,
        "postiDisponibili": 20
    },
    "The Car": {
        "nomeArtista": "Arctic Monkeys",
        "data": "03/02/2026",
        "prezzoBiglietto": 90,
        "postiDisponibili": 7
    },
    "Damn": {
        "nomeArtista": "Kendrick Lamar",
        "data": "23/08/2026",
        "prezzoBiglietto": 120,
        "postiDisponibili": 31
    },
}


def initServerSocket(address, port):
    """Crea e configura il socket del server, lo associa all'indirizzo e porta specificati e si mette in ascolto."""
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((address, port))
    serverSocket.listen(5)
    print(f"Server in ascolto sulla porta {port}...")
    return serverSocket


def sendConcertiData(client, concerti):
    """Invia il catalogo concerti come stringa JSON al client."""
    data = json.dumps(concerti)
    client.sendall(data.encode())


def receivePurchaseData(client):
    """Riceve dal client i dati di acquisto nel formato 'concerto|quantità' e li salva nelle variabili globali."""
    global selectedConcerto, selectedConcertoBiglietti
    data = client.recv(1024).decode()
    selectedConcerto, selectedConcertoBiglietti = data.split("|")
    selectedConcertoBiglietti = int(selectedConcertoBiglietti)


def calculatePurchasePrice():
    """Calcola il prezzo totale in base alla quantità richiesta.
       Se la quantità supera la metà dei biglietti disponibili, applica uno sconto:
       un biglietto viene regalato (sottrae il prezzo di un biglietto)."""
    scontoApplicato = False
    concertoPrice = concerti[selectedConcerto]["prezzoBiglietto"]
    bigliettiConcerto = concerti[selectedConcerto]["postiDisponibili"]

    if selectedConcertoBiglietti > (bigliettiConcerto / 2):
        scontoApplicato = True
        # Sconto: un biglietto omaggio
        return (concertoPrice * selectedConcertoBiglietti) - concertoPrice, scontoApplicato

    return concertoPrice * selectedConcertoBiglietti, scontoApplicato


def sendScontrino(client):
    """Invia al client l'importo totale e un flag che indica se lo sconto è stato applicato."""
    purchaseValue, scontoApplicato = calculatePurchasePrice()
    if scontoApplicato:
        client.sendall(f"{purchaseValue}|True".encode())
    else:
        client.sendall(f"{purchaseValue}|False".encode())


if __name__ == "__main__":
    # Avvio del server su localhost porta 9090
    serverSocket = initServerSocket('127.0.0.1', 9090)
    while True:
        # Accetta una connessione in entrata
        conn, addr = serverSocket.accept()
        print(f'Connessione stabilita con: {addr}')

        # Fasi della comunicazione con il client:
        # 1. invio catalogo concerti
        sendConcertiData(conn, concerti)
        # 2. ricezione richiesta di acquisto
        receivePurchaseData(conn)
        # 3. calcolo e invio dello scontrino
        sendScontrino(conn)
