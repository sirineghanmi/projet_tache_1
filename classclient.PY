import socket
import json
import argparse
import sys
import time
from typing import Optional, Any, Dict, List

BUFFER_SIZE = 65536
ENC = 'utf-8'

#!/usr/bin/env python3
"""
client_simplifie.py
Version simplifiee du client CLI pour le mini-projet RSI2.
But: garder le protocole JSON sur TCP mais avec un code court et lisible.
Usage:
    python client_simplifie.py --host 127.0.0.1 --port 5000
"""
import socket
import json
import argparse

BUFFER_SIZE = 4096
ENC = 'utf-8'

class ClientTachesSimple:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def _connect(self):
        if self.sock:
            return True
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=5)
            return True
        except Exception as e:
            print(f"Erreur connexion: {e}")
            self.sock = None
            return False

    def _send_recv(self, obj):
        if not self._connect():
            return None
        try:
            msg = (json.dumps(obj, ensure_ascii=False) + "\n").encode(ENC)
            self.sock.sendall(msg)

            # lire jusqu'au \n
            data = b""
            while True:
                chunk = self.sock.recv(BUFFER_SIZE)
                if not chunk:
                    print("Serveur fermé la connexion")
                    self.close()
                    return None
                data += chunk
                if b"\n" in chunk:
                    break
            line, _sep, _rest = data.partition(b"\n")
            return json.loads(line.decode(ENC))
        except Exception as e:
            print(f"Erreur envoi/reception: {e}")
            self.close()
            return None

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.sock = None

    # actions
    def add(self, titre, description, auteur='inconnu'):
        resp = self._send_recv({"action": "add", "titre": titre, "description": description, "auteur": auteur})
        print(resp or "Pas de réponse")

    def list(self, statut=None):
        req = {"action": "list"}
        if statut:
            req['statut'] = statut
        resp = self._send_recv(req)
        if not resp:
            print("Pas de réponse")
            return
        if not resp.get('ok'):
            print("Erreur:", resp.get('msg'))
            return
        for t in resp.get('data', []):
            print(f"{t.get('id')} - {t.get('titre')} [{t.get('statut')}] par {t.get('auteur')}")

    def delete(self, tid):
        resp = self._send_recv({"action": "del", "id": tid})
        print(resp or "Pas de réponse")

    def status(self, tid, statut):
        statut = statut.upper()
        if statut not in ("TODO", "DOING", "DONE"):
            print("Statut invalide")
            return
        resp = self._send_recv({"action": "status", "id": tid, "statut": statut})
        print(resp or "Pas de réponse")


def menu(cli):
    try:
        while True:
            print('\n1) Ajouter  2) Lister  3) Supprimer  4) Changer statut  0) Quitter')
            c = input('> ').strip()
            if c == '1':
                t = input('Titre: ').strip()
                d = input('Description: ').strip()
                a = input('Auteur: ').strip() or 'inconnu'
                cli.add(t, d, a)
            elif c == '2':
                s = input('Filtrer par statut (vide pour tout): ').strip()
                cli.list(s or None)
            elif c == '3':
                i = input('ID: ').strip()
                if i.isdigit():
                    cli.delete(int(i))
                else:
                    print('ID invalide')
            elif c == '4':
                i = input('ID: ').strip()
                st = input('Statut (TODO/DOING/DONE): ').strip()
                if i.isdigit():
                    cli.status(int(i), st)
                else:
                    print('ID invalide')
            elif c == '0':
                break
            else:
                print('Choix inconnu')
    except KeyboardInterrupt:
        print('\nFin')
    finally:
        cli.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=5000)
    args = p.parse_args()

    client = ClientTachesSimple(host=args.host, port=args.port)
    menu(client)

