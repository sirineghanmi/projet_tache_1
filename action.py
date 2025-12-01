# action.py
import argparse
from classclient import ClientTachesSimple

def _call_list(cli, statut):
    if hasattr(cli, 'list'):
        try:
            return cli.list(statut)
        except TypeError:
            return cli.list()
    elif hasattr(cli, 'list_tasks'):
        try:
            return cli.list_tasks(statut)
        except TypeError:
            return cli.list_tasks()
    else:
        print("Méthode de listing introuvable dans le client.")

def menu(cli):
    try:
        while True:
            # Affichage du menu — une option par ligne
            print('\n1) Ajouter\n2) Lister\n3) Supprimer\n4) Changer statut\n0) Quitter')
            c = input('> ').strip()
            if c == '1':
                t = input('Titre: ').strip()
                d = input('Description: ').strip()
                a = input('Auteur: ').strip() or 'inconnu'
                if hasattr(cli, 'add'):
                    cli.add(t, d, a)
                else:
                    print("Méthode add introuvable dans le client.")
            elif c == '2':
                s = input('Filtrer par statut (vide pour tout): ').strip()
                _call_list(cli, s or None)
            elif c == '3':
                i = input('ID: ').strip()
                if i.isdigit():
                    if hasattr(cli, 'delete'):
                        cli.delete(int(i))
                    else:
                        print("Méthode delete introuvable dans le client.")
                else:
                    print('ID invalide')
            elif c == '4':
                i = input('ID: ').strip()
                st = input('Statut (TODO/DOING/DONE): ').strip()
                if i.isdigit():
                    if hasattr(cli, 'status'):
                        cli.status(int(i), st)
                    else:
                        print("Méthode status introuvable dans le client.")
                else:
                    print('ID invalide')
            elif c == '0':
                break
            else:
                print('Choix inconnu')
    except KeyboardInterrupt:
        print('\nFin')
    finally:
        if hasattr(cli, 'close'):
            cli.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=5000)
    args = p.parse_args()

    client = ClientTachesSimple(host=args.host, port=args.port)
    menu(client)
