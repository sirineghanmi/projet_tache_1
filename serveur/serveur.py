import socket
from gestionaire import GestionnaireTaches

HOST = "127.0.0.1"
PORT = 5000

gest = GestionnaireTaches()

def traiter(msg):
    parts = msg.split(";")

    action = parts[0]

    if action == "ADD":
        titre = parts[1]
        desc = parts[2]
        auteur = parts[3]
        t = gest.ajouter_tache(titre, desc, auteur)
        return f"OK;{t.id}"

    elif action == "LIST":
        if not gest.taches:
            return "EMPTY"
        lignes = []
        for t in gest.taches:
            lignes.append(f"{t.id}:{t.titre}:{t.statut}:{t.auteur}")
        return "|".join(lignes)

    elif action == "DEL":
        id = int(parts[1])
        if gest.supprimer_tache(id):
            return "OK"
        return "NOT_FOUND"

    elif action == "STATUS":
        id = int(parts[1])
        statut = parts[2]
        if gest.changer_statut(id, statut):
            return "OK"
        return "NOT_FOUND"

    return "UNKNOWN"
    

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
print("Serveur en écoute...")

while True:
    conn, addr = sock.accept()
    print("Client connecté:", addr)

    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            rep = traiter(data)
            conn.sendall(rep.encode())
