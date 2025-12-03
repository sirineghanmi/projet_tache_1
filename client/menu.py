from client import ClientTaches

cli = ClientTaches()

while True:
    print("\n1. Ajouter")
    print("2. Lister")
    print("3. Supprimer")
    print("4. Changer statut")
    print("0. Quitter")

    c = input("> ")

    if c == "1":
        t = input("Titre: ")
        d = input("Description: ")
        a = input("Auteur: ")
        rep = cli.envoyer(f"ADD;{t};{d};{a}")
        print("Réponse:", rep)

    elif c == "2":
        rep = cli.envoyer("LIST;")
        print(rep)

    elif c == "3":
        id = input("ID: ")
        rep = cli.envoyer(f"DEL;{id}")
        print("Réponse:", rep)

    elif c == "4":
        id = input("ID: ")
        st = input("Statut (TODO/DOING/DONE): ")
        rep = cli.envoyer(f"STATUS;{id};{st}")
        print("Réponse:", rep)

    elif c == "0":
        cli.close()
        break
