# PROJET MESSAGERIE
# Aguesse Nathan L2-Y N°21001877
# Sinnaththurai Sriram L2-Y N°21002831

import socket
import threading
import tkinter as tk
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 54321

class Client:
    def __init__(self, master):
        self.master = master
        master.geometry("500x300")
        master.title("Chat Client")
        
        # Crée un cadre pour afficher les messages
        self.message_frame = tk.Frame(master)
        self.message_frame.pack(padx=10, pady=10)

        # Ajoute une barre de défilement à la liste des messages
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crée une liste pour afficher les messages
        self.message_list = tk.Listbox(self.message_frame, yscrollcommand=self.scrollbar.set, width=450)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure la barre de défilement pour fonctionner avec la liste des messages
        self.scrollbar.config(command=self.message_list.yview)

         # Crée un champ de texte pour saisir les messages
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(pady=10)

        # Crée des boutons pour quitter et changer le nom de l'utilisateur
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)
        self.quit_button = tk.Button(self.button_frame, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.change_name_button = tk.Button(self.button_frame, text="Changer de nom", command=self.change_name)
        self.change_name_button.pack(side=tk.RIGHT)

        # Associe la touche "Entrée" à la méthode "send"
        self.master.bind("<Return>", self.send)
        
        # Initialise le nom de l'utilisateur et crée une socket pour communiquer avec le serveur
        self.name = "Anonyme"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se connecte au serveur et envoie le nom de l'utilisateur
        self.client_socket.connect((HOST, PORT))
        self.client_socket.sendall(bytes(self.name, 'utf-8'))

        # Lance un thread pour recevoir les messages du serveur
        threading.Thread(target=self.receive).start()


    # Reçoit les messages du serveur en continu et les affiche dans la liste de messages de l'interface
    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.message_list.insert(tk.END, message)
            except:
                break
    
    # Récupère le message saisi par l'utilisateur et l'envoie au serveur
    def send(self, event):
        message = self.entry.get()
        if message == "quitter": # Si l'utilisateur saisit "quitter", ferme la socket et quitte l'application
            self.client_socket.close()
            self.master.quit()
        else:  # Sinon, envoie le message au serveur et vide le champ de texte
            self.client_socket.sendall(bytes(message, 'utf-8'))
            self.entry.delete(0, tk.END)
    
    # Envoie un message spécial "quitter" au serveur, ferme la socket et quitte l'application
    def quit(self):
        self.client_socket.sendall(bytes("quitter", 'utf-8'))
        self.client_socket.close()
        self.master.quit()


    # Lorsque l'utilisateur clique sur le bouton Changer de nom
    def change_name(self):
        self.name = tk.simpledialog.askstring("Changer de nom", "Entrez votre nouveau nom:")
        self.client_socket.sendall(bytes(f"[nameChange] {self.name}", 'utf-8'))

root = tk.Tk()
client = Client(root)
root.mainloop()
