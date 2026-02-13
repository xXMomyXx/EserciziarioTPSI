import socket
import json
import tkinter as tk

# Variabili globali per memorizzare il film selezionato e il numero di biglietti
# (riutilizzata prima per i biglietti disponibili, poi per quelli richiesti)
selectedMovie = ""
selectedMovieBiglietti = 0


def initClientSocket():
    """Inizializzazione lato client della socket su localhost porta 8080."""
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('localhost', 8080))
    return clientSocket


def receiveMoviesData(client):
    """Riceve dal server il dizionario dei film in formato JSON e lo decodifica."""
    data = client.recv(4096).decode()
    movies = json.loads(data)
    return movies


def rootInit():
    """Inizializzazione della finestra principale Tkinter.
       Mostra la lista dei film e i pulsanti per visualizzare le informazioni."""
    # Creazione finestra principale
    root = tk.Tk()
    root.title('Biglietteria cinematografica')
    root.geometry('300x300')

    # Etichetta di istruzione
    selectLabel = tk.Label(root, text='Seleziona un film per acquistarne i biglietti')
    selectLabel.pack(padx=10, pady=10)

    # Listbox contenente i titoli dei film
    movieListbox = tk.Listbox(root, selectmode=tk.SINGLE, height=len(movies))
    movieListbox.pack(padx=10, pady=10)
    for movie in movies:
        movieListbox.insert(tk.END, movie)

    # Pulsante per visualizzare le informazioni del film selezionato
    infoButton = tk.Button(root, text='Visualizza info film',
                           command=lambda: getSelectedMovie(movieListbox, movies, infoLabel, selectionButton))
    infoButton.pack(padx=10, pady=10)

    # Etichetta che mostrerà prezzo e biglietti disponibili
    infoLabel = tk.Label(root, text="")
    infoLabel.pack(padx=10, pady=10)

    # Pulsante per procedere all'acquisto (inizialmente non visibile)
    selectionButton = tk.Button(root, text='Acquista', command=lambda: bigliettiInterface(root))
    # Il pulsante viene visualizzato solo dopo la selezione di un film

    root.mainloop()


def getSelectedMovie(listbox, movies, infoLabel, selectionButton):
    """Recupera il film selezionato dalla Listbox, aggiorna le variabili globali
       e mostra le informazioni (prezzo e biglietti disponibili)."""
    global selectedMovie, selectedMovieBiglietti
    selectedIndex = listbox.curselection()
    if selectedIndex:
        selectedMovie = listbox.get(selectedIndex[0])
        prezzo = movies[selectedMovie]["prezzo"]
        selectedMovieBiglietti = movies[selectedMovie]["biglietti"]
        infoLabel.config(text=f"Prezzo: {prezzo} €\nBiglietti disponibili: {selectedMovieBiglietti}")
        # Mostra il pulsante "Acquista" solo dopo aver selezionato un film
        selectionButton.pack(padx=10, pady=10)
    else:
        infoLabel.config(text="Seleziona un film per visualizzare le informazioni")


def getSelectedBigliettoNumber(listbox):
    """Legge dalla Listbox il numero di biglietti scelto dall'utente.
       La variabile globale selectedMovieBiglietti viene riutilizzata
       per contenere ora la quantità richiesta."""
    global selectedMovieBiglietti
    selectedIndex = listbox.curselection()
    selectedMovieBiglietti = listbox.get(selectedIndex[0])


def sendPurchaseData(listbox, root):
    """Invia al server i dati di acquisto nel formato 'film|quantità'."""
    getSelectedBigliettoNumber(listbox)
    clientSocket.sendall(f"{selectedMovie}|{selectedMovieBiglietti}".encode())
    # Pulisce la finestra per preparare la visualizzazione dello scontrino
    clearWindow(root)


def showPurchaseButton(event, purchaseButton):
    """Mostra il pulsante di acquisto quando l'utente seleziona un numero di biglietti."""
    purchaseButton.pack(padx=10, pady=10)


def clearWindow(root):
    """Distrugge tutti i widget presenti nella finestra."""
    for widget in root.winfo_children():
        widget.destroy()


def bigliettiInterface(root):
    """Interfaccia per la selezione del numero di biglietti da acquistare."""
    clearWindow(root)
    root.geometry('350x300')

    # Etichetta che mostra il film selezionato
    ticketNumberLabel = tk.Label(root, text=f"Quanti biglietti per {selectedMovie} vuoi acquistare?")
    ticketNumberLabel.pack(padx=10, pady=10)

    # Listbox con i numeri da 1 fino ai biglietti disponibili
    ticketListbox = tk.Listbox(root, selectmode=tk.SINGLE, height=selectedMovieBiglietti)
    for i in range(1, selectedMovieBiglietti + 1):
        ticketListbox.insert(tk.END, i)
    ticketListbox.pack(padx=10, pady=10)

    # Pulsante per confermare l'acquisto (inizialmente non visibile)
    purchaseButton = tk.Button(root, text='Acquista',
                               command=lambda: scontrinoInterface(ticketListbox, root))

    # Evento <<ListboxSelect>>: quando si seleziona un numero, compare il pulsante
    ticketListbox.bind("<<ListboxSelect>>", lambda event: showPurchaseButton(event, purchaseButton))


def receiveScontrino():
    """Riceve dal server il totale speso e l'eventuale sconto applicato."""
    data = clientSocket.recv(1024).decode()
    purchaseValue, scontoApplicato = data.split("|")
    return purchaseValue, scontoApplicato


def scontrinoInterface(listbox, root):
    """Invia i dati di acquisto, riceve la risposta e mostra lo scontrino."""
    sendPurchaseData(listbox, root)
    purchaseValue, scontoApplicato = receiveScontrino()

    # Ringraziamento e dettagli dell'acquisto
    thanksLabel = tk.Label(root, text="Grazie per l'acquisto!")
    thanksLabel.pack(padx=10, pady=10)

    scontrinoLabel = tk.Label(root)
    scontrinoLabel.pack(padx=10, pady=10)

    if scontoApplicato == 'True':
        scontrinoLabel.config(text=f"Hai ricevuto un biglietto in omaggio!\nPrezzo totale acquisto: {purchaseValue} €")
    else:
        scontrinoLabel.config(text=f"Prezzo totale acquisto: {purchaseValue} €")


if __name__ == '__main__':
    # Avvio del client: connessione al server, ricezione catalogo film e avvio GUI
    clientSocket = initClientSocket()
    movies = receiveMoviesData(clientSocket)
    rootInit()
