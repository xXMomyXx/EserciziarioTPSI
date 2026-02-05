import socket

# Creiamo una lista contenente a sua volta all'interno altre liste in cui abbiamo:
# Primo indice: Nome film
# Secondo indice: Numero di biglietti disponibili
# Terzo indice: Prezzo biglietto singolo
listaFilm = [
    ["Il signore degli anelli|", "5|", "6|"],
    ["Oppenheimer|", "3|", "8.5|"],
    ["Interstellar|", "12|", "9|"],
    ["Il padrino|", "4|", "7|"],
    ["Avengers Endgame|", "5|", "5|"]
]

def initServerSocket(address, port):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((address,port))
    serverSocket.listen(5)
    print(f"Server in ascolto sulla porta {port}...")
    return serverSocket

def sendMoviesData(client, movies):
    for movie in movies:
        for element in movie:
            client.sendall(element.encode())
    client.sendall('end'.encode())


if __name__ == '__main__':
    serverSocket = initServerSocket('127.0.0.1',8080)
    while True:
        conn, addr = serverSocket.accept()
        print(f'Connessione stabilita con: {addr}')
        sendMoviesData(conn, listaFilm)
