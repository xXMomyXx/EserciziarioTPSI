import socket
import tkinter as tk
from tkinter import messagebox

# Inizializzazione lato client della socket su porta 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Funzione di inserimento per mandare richieste al server
def start_client():
        print("-----CENTRALE TAXI------\n")
        # Inserimento città di partenza e di arrivo
        partenza = entry1.get()
        arrivo = entry2.get()
        if partenza.isdigit() or arrivo.isdigit():
            print("Inserimento invalido. Reinserire")
            return
        # Unione di città di partenza e arrivo in un unica stringa separate da '|'
        message = f"{partenza}|{arrivo}"
        # Invio della stringa sotto forma di sequenza di byte (encode())
        client_socket.sendall(message.encode())
        # Ricezione risposta server e decodifica della sequenza di byte (decode())
        response = client_socket.recv(1024).decode()
        # Presentazione su schermo della risposta ricevuta
        messagebox.showinfo("Risposta del server",response)
        # Finita la disponibilità di taxi si chiude il lato client della socket
        if response == 'Non ci sono più taxi disponibili. Server in chiusura.':
            client_socket.close()
            root.destroy()


# Chiamata della funzione 'start_client' in main attraverso il 'button' di Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.title("CENTRALE TAXI")
    root.geometry("300x200")

    label1 = tk.Label(root,text = "Inserisci la città di partenza")
    label1.pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)
    label2 = tk.Label(root,text = "Inserisci la città di destinazione")
    label2.pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)
    button = tk.Button(root,text="Invia richiesta",command=start_client)
    button.pack(pady=10)
    root.mainloop()
