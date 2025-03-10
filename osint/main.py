import argparse

from utils.utils import save_result_to_file
from searchers.username.username import search_username
from searchers.ip_lookup.ip_lookup import search_ip_address
from searchers.full_name.search_engine import search_full_name

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
        print("\n\n", result)
        save_result_to_file(result)
    elif args.ip:
        result = search_ip_address(args.ip)
        print("\n\n", result)
        save_result_to_file(result)
    else:
        result = search_username(args.u)
        print("\n\n", result)
        save_result_to_file(result)
    


if __name__ == "__main__":
    main()

