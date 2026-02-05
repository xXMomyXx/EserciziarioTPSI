import socket
import tkinter as tk
from tkinter import messagebox
listaFilm = []

def initClientSocket():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('localhost', 8080))
    return clientSocket

def receiveMoviesData(client):
    movieList = []
    fullMessage = ''
    while True:
        data = client.recv(1024).decode()
        fullMessage += data
        if 'end' in fullMessage:
            break
    while '|' in fullMessage:
        message, fullMessage = fullMessage.split('|', 1)
        if message == 'end':
            break
        movieList.append(message)
    finalMovieList = []
    for i in range(0, len(movieList), 3):
        # [i:i+3]: Prende una sottolista di 3 elementi a partire dall'indice i e la aggiunge alla lista finale
        finalMovieList.append(movieList[i:i+3])
    return finalMovieList

def rootInit(): #Da definire funzione per inizializzare root
    return

if __name__ == '__main__':
    root = tk.Tk()
    clientSocket = initClientSocket()
    listaFilm = receiveMoviesData(clientSocket)
    print(listaFilm)
    clientSocket.close()
