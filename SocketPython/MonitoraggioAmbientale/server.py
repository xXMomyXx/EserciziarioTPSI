import socket


# Funzione per gestire ogni connessione client individualmente
def centralInstance(conn, addr):
    # Buffer per accumulare dati ricevuti
    messageContainer = ""
    # Lista per messaggi completi (separati da punto)
    messages = []
    # Flag per terminare ciclo di ricezione
    breakCondition = False
    print(f"Connessione stabilita con {addr}")

    # Loop che riceve i dati dal client finché non riceve "fine"
    while True:
        data = conn.recv(1024)
        if not data:
            break
        # Decodifica e accumulo nel buffer
        messageContainer += data.decode()
        # Estrazione di messaggi completi
        while '.' in messageContainer:
            message, messageContainer = messageContainer.split(".", 1)
            messages.append(message)
            if message == 'fine':
                breakCondition = True
        if breakCondition:
            break

    # Liste per estrarre date e temperature dai messaggi
    dates = []
    temps = []
    for message in messages:
        if message == "fine":
            continue
        # Divisione di ogni messaggio nei suoi componenti
        giorno, temp12, temp24 = message.split("|")
        dates.append(giorno)
        temps.append(int(temp12))
        temps.append(int(temp24))

    # Calcolo statistiche: media arrotondata, temperatura minima e massima
    media, tempMin, tempMax = round(sum(temps) / len(temps)), min(temps), max(temps)
    # Costruzione risposta nel formato: media|min|max
    response = f"{media}|{tempMin}|{tempMax}"
    # Invio risposta al client
    conn.sendall(response.encode())
    conn.close()
    print(f"Connessione terminata con {addr}")


def start_server():
    # Inizializzazione lato server della socket su porta 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server in ascolto sulla porta 12345...")

    # Accettazione di una singola connessione (senza molteplici thread)
    conn, addr = server_socket.accept()
    # Gestione della connessione accettata
    centralInstance(conn, addr)


# Chiamata della funzione 'start_server' in main
if __name__ == "__main__":
    start_server()
