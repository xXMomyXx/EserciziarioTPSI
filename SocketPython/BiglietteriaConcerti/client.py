import socket
import json
import tkinter as tk
from tkinter import StringVar

selectedConcerto = ""
selectedConcertoBiglietti = 0


def initClientSocket():
    """Inizializza il socket client sulla porta 9090 di localhost e si connette al server."""
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('localhost', 9090))
    return clientSocket


def receiveConcertiData(clientSocket):
    """Riceve il catalogo concerti dal server e lo decodifica da JSON."""
    data = clientSocket.recv(1024)
    concerti = json.loads(data)
    return concerti


def getSelectedConcerto(listbox, concerti, infoLabel, selectionButton):
    """Recupera il concerto selezionato dalla Listbox, aggiorna le variabili globali
       e mostra le informazioni (prezzo e biglietti disponibili)."""
    global selectedConcerto, selectedConcertoBiglietti
    selectedIndex = listbox.curselection()
    if selectedIndex:
        selectedConcerto = listbox.get(selectedIndex[0])
        nomeArtista = concerti[selectedConcerto]["nomeArtista"]
        data = concerti[selectedConcerto]["data"]
        prezzoBiglietto = concerti[selectedConcerto]["prezzoBiglietto"]
        selectedConcertoBiglietti = concerti[selectedConcerto]["postiDisponibili"]
        infoLabel.config(
            text=f"Nome artista: {nomeArtista}\nData: {data}\nPrezzo biglietto: {prezzoBiglietto}€\nPosti disponibili: {selectedConcertoBiglietti}")
        # Mostra il pulsante "Acquista" solo dopo aver selezionato un concerto
        selectionButton.pack(padx=10, pady=10)
    else:
        infoLabel.config(text="Seleziona un concerto per visualizzarne le informazioni")


def clearWindow(root):
    """Distrugge tutti i widget presenti nella finestra."""
    for widget in root.winfo_children():
        widget.destroy()


def bigliettiInterface(root):
    """Interfaccia per la selezione del numero di biglietti da acquistare."""
    clearWindow(root)

    # Etichetta che mostra il concerto selezionato
    ticketNumberLabel = tk.Label(root, text=f"Quanti biglietti per {selectedConcerto} vuoi acquistare?")
    ticketNumberLabel.pack(padx=10, pady=10)

    # OptionMenu con i numeri da 1 fino ai biglietti disponibili
    defaultOption = StringVar(value="1")
    ticketDropdown = tk.OptionMenu(root, defaultOption, *range(1, selectedConcertoBiglietti + 1),
                                   command=lambda value: assignBigliettoNumber(value))
    ticketDropdown.pack(padx=10, pady=10)
    # Pulsante per confermare l'acquisto
    purchaseButton = tk.Button(root, text='Acquista',
                               command=lambda: scontrinoInterface(root))
    purchaseButton.pack(padx=10, pady=10)


def sendPurchaseData(root):
    """Invia al server i dati di acquisto nel formato 'concerto|quantità'."""
    clientSocket.sendall(f"{selectedConcerto}|{selectedConcertoBiglietti}".encode())
    # Pulisce la finestra per preparare la visualizzazione dello scontrino
    clearWindow(root)


def assignBigliettoNumber(value):
    """Legge dall'OptionMenu il numero di biglietti scelto dall'utente.
       La variabile globale selectedConcertoBiglietti viene riutilizzata
       per contenere ora la quantità richiesta."""
    global selectedConcertoBiglietti
    selectedConcertoBiglietti = value


def receiveScontrino():
    """Riceve dal server il totale speso e l'eventuale sconto applicato."""
    data = clientSocket.recv(1024).decode()
    purchaseValue, scontoApplicato = data.split("|")
    return purchaseValue, scontoApplicato


def scontrinoInterface(root):
    """Invia i dati di acquisto, riceve la risposta e mostra lo scontrino."""
    sendPurchaseData(root)
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


def rootInit():
    """Inizializzazione della finestra principale Tkinter.
       Mostra la lista dei concerti e i pulsanti per visualizzare le informazioni."""
    # Creazione finestra principale
    root = tk.Tk()
    root.title('Biglietteria concerti')

    # Etichetta di istruzione
    selectLabel = tk.Label(root, text='Seleziona un concerto per acquistarne i biglietti')
    selectLabel.pack(padx=10, pady=10)

    # Listbox contenente i titoli dei concerti
    concertiListbox = tk.Listbox(root, selectmode=tk.SINGLE, height=len(concerti))
    concertiListbox.pack(padx=10, pady=10)
    for concerto in concerti:
        concertiListbox.insert(tk.END, concerto)

    # Pulsante per visualizzare le informazioni del concerto selezionato
    infoButton = tk.Button(root, text='Visualizza info concerto',
                           command=lambda: getSelectedConcerto(concertiListbox, concerti, infoLabel, selectionButton))
    infoButton.pack(padx=10, pady=10)

    # Etichetta che mostrerà prezzo e biglietti disponibili
    infoLabel = tk.Label(root, text="")
    infoLabel.pack(padx=10, pady=10)

    # Pulsante per procedere all'acquisto (inizialmente non visibile)
    selectionButton = tk.Button(root, text='Acquista', command=lambda: bigliettiInterface(root))
    # Il pulsante viene visualizzato solo dopo la selezione di un concerto

    root.mainloop()


if __name__ == "__main__":
    clientSocket = initClientSocket()
    concerti = receiveConcertiData(clientSocket)
    rootInit()
