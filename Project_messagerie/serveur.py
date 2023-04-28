# PROJET MESSAGERIE
# Aguesse Nathan L2-Y N°21001877
# Sinnaththurai Sriram L2-Y N°21002831

import signal
import sys
import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 54321
CAPACITY = 2
userList = []


def main():
    # Préparation du serveur...
    print("Server started...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(CAPACITY)
    threadAddingUsers = Thread(target=waitingUsers, args=[s])
    threadAddingUsers.daemon = True
    threadAddingUsers.start()
    print("Starting to wait for users...")
    signal.signal(signal.SIGINT, exitSignal)
    while True:
        pass

def waitingUsers(s):
    # Thread permettant la constante arrivé d'utilisateur, jusqu'à atteindre la capacité maximale
    while True:
        while len(userList) < CAPACITY:
            user, address = s.accept()
            userList.append(user)
            connexion(user)

def connexion(user):
    # On obtient le nom de l'utilisateur, puis on démare sa thread
    name = str(user.recv(1024), 'utf-8')
    log(f"< {name} connecté >", name, True)
    threadUser = Thread(target=recepUser, args=(user, name))
    threadUser.start()
    
def recepUser(user, name):
    # Thread pour chaque utilisateur, renvoie constamment les messages qu'il envoie à tout les utilisateurs
    while True:
        userMsg = user.recv(1024)
        if str(userMsg, 'utf-8') == 'quitter' or not userMsg:
            break
        if str(userMsg, 'utf-8').startswith("[nameChange]"):
            name = str(userMsg, 'utf-8')[13:]
            continue
        log(userMsg, name, False)
    userList.remove(user)
    log(f"< {name} déconnecté >", name, True)

def log(msg, name, serverAnnouncement):
    # Envoie un message à tout les utilisateurs, en fonction que cela soit un message normal ou non, mettra le nom de l'utilisateur avant le message
    if serverAnnouncement:
        print(msg)
        for user in userList:
            user.sendall(bytes(msg, 'utf-8'))
    else:
        print(f"{name}: {str(msg,'utf-8')}")
        for user in userList:
            user.sendall(bytes(f"{name}: {str(msg, 'utf-8')}", 'utf-8'))

def exitSignal(signal, frame):
    if not userList:
        print("Fermeture du serveur...")
        sys.exit(0)
    else:
        print("[SERVER ONLY MESSAGE] Ne peut pas quitter lorsque au moins 1 utilisateur est connecté")
    

if __name__ == '__main__':
    main()