import argparse

from searchers.full_name import search_full_name

def main():
    parser = argparse.ArgumentParser(description='Welcome to passive v1.0.0')
    parser.add_argument('-fn', type=str, help='Search with full-name')
    parser.add_argument('-ip', type=str, help='Search with ip address')
    parser.add_argument('-u', type=str, help='Search with username')

    args = parser.parse_args()

    if not any([args.fn, args.ip, args.u]):
        print("Veuillez spécifier une option valide (-fn, -ip, -u)")
        return

    if args.fn:
        result = search_full_name(args.fn)
        # enregistrer les resultats dans un fichier
        print("search with full name:", result)
    elif args.ip:
        #result = appel de la fonction Search with ip address
        # enregistrer les resultats dans un fichier
        print("Search with ip address")
    else:
        #result = appel de la fonction Search with username
        # enregistrer les resultats dans un fichier
        print("Search with username")
    


if __name__ == "__main__":
    main()

