import socket
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Inizializzazione lato client della socket su porta 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
nGiorni, counter = 0, 0
daysData = []


def getNumDays(start_window, entry):
    global nGiorni
    try:
        giorni = int(entry.get())
        if giorni <= 0:
            raise ValueError("Il numero di giorni deve essere maggiore di zero")
    except ValueError:
        messagebox.showinfo("Errore", "Il numero di giorni deve essere in formato numerico e maggiore di zero")
        return
    nGiorni = giorni
    start_window.destroy()
    root.deiconify()


# Funzione che itera per ogni elemento all'interno di una finestra e se sono di tipo 'Entry' li svuota
def clearEntries(window):
    for widget in window.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, 'end')


# Funzione di inserimento per mandare richieste al server
def mainInterfaceLogic(entry1, entry2, entry3):
    global daysData, counter
    # Inserimento città di partenza e di arrivo
    giorno = entry1.get()
    try:
        datetime.strptime(giorno, "%d/%m/%Y")
    except ValueError:
        messagebox.showinfo("Errore", "Formato non valido. Usa GG/MM/AAAA")
        return
    try:
        temp12 = int(entry2.get())
        temp24 = int(entry3.get())
    except ValueError:
        messagebox.showinfo("Errore", "Le temperature devono essere in formato numerico")
        return
    # Unione di città di partenza e arrivo in un unica stringa separate da '|'
    message = f"{giorno}|{temp12}|{temp24}."
    daysData.append(message)
    counter += 1
    # Operatore ternario: Finito l'inserimento dei giorni la finestra viene chiusa, altrimenti si svuotano gli spazi di
    # inserimento in preparazione del prossimo inserimento
    root.withdraw(), sendData(daysData), result_window.deiconify if counter == nGiorni else clearEntries(root)


def sendData(data):
    for message in data:
        # Invio della stringa sotto forma di sequenza di byte (encode())
        client_socket.sendall(message.encode())
    # Ricezione risposta server e decodifica della sequenza di byte (decode())
    response = client_socket.recv(1024).decode()
    # Presentazione su schermo della risposta ricevuta
    messagebox.showinfo("Risposta del server", response)
    # Finita la disponibilità di taxi si chiude il lato client della socket
    if response:
        client_socket.close()


def startWindowInit():
    start_window = tk.Toplevel(root)
    start_window.title("Invio Temperature Giornaliere – Stazione Meteo")
    label = tk.Label(start_window, text="Per quanti giorni vuoi inserire i dati?")
    label.pack(pady=5)
    entry = tk.Entry(start_window)
    entry.pack(pady=5)
    button = tk.Button(start_window, text="Conferma", command=lambda: getNumDays(start_window, entry))
    button.pack(pady=10)
    start_window.geometry("500x100")


def rootInit():
    root.geometry("300x250")
    label1 = tk.Label(root, text="Inserisci il giorno di rilevazione (GG/MM/AAAA)")
    label1.pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)
    label2 = tk.Label(root, text="Inserisci la temperatura rilevata alle ore 12:00")
    label2.pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)
    label3 = tk.Label(root, text="Inserisci la temperatura rilevata alle ore 24:00")
    label3.pack(pady=5)
    entry3 = tk.Entry(root)
    entry3.pack(pady=5)
    button1 = tk.Button(root, text="Invia dati", command=lambda: mainInterfaceLogic(entry1, entry2, entry3))
    button1.pack(pady=10)


def resultWindowInit(midTemp, maxTemp, minTemp):  # Da rendere max, min, e med temp come argomenti ricevuti dal server
    resultWindow = tk.Toplevel(root)
    resultWindow.title("Risultati")
    label = tk.Label(resultWindow, text=f"Numero giorni analizzati: {nGiorni}")
    label.pack(pady=5)
    label1 = tk.Label(resultWindow, text=f"Numero rilevazioni fatte: {nGiorni * 2}")
    label1.pack(pady=5)
    label1 = tk.Label(resultWindow, text=f"Temperatura media: {midTemp}")
    label1.pack(pady=5)
    label1 = tk.Label(resultWindow, text=f"Temperatura massima: {maxTemp}")
    label1.pack(pady=5)
    label1 = tk.Label(resultWindow, text=f"Temperatura minima: {minTemp}")
    label1.pack(pady=5)
    return resultWindow


# Chiamata della funzione 'start_client' in main attraverso il 'button' di Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    startWindowInit()
    rootInit()
    result_window = resultWindowInit(10, 10, 10)
    result_window.withdraw()
    root.mainloop()

# Da fixare chiusura istantanea prima interfaccia GUI dopo pressione bottone
