import argparse

from threading import Thread
from flask import Flask, request, jsonify, render_template

from utils.utils import save_result_to_file
from searchers.username.username import search_username
from searchers.ip_lookup.ip_lookup import search_ip_address
from searchers.full_name.search_engine import search_full_name

app = Flask(__name__, template_folder='view/templates', static_folder='view/static')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/search', methods=['GET'])
def search_api():
    fn = request.args.get('fn')
    ip = request.args.get('ip')
    username = request.args.get('u')

    if not any([fn, ip, username]):
        return jsonify({"error": "Veuillez spécifier une option valide (-fn, -ip, -u)"}), 400

    if fn:
        result = search_full_name(fn)
        save_result_to_file(result)
        return jsonify({"result": result})
    elif ip:
        result = search_ip_address(ip)
        save_result_to_file(result)
        return jsonify({"result": result})
    elif username:
        result = search_username(username)
        save_result_to_file(result)
        return jsonify({"result": result})

def run_flask():
    app.run(debug=True, use_reloader=False)


def main():
    parser = argparse.ArgumentParser(description='Welcome to passive v1.0.0')
    parser.add_argument('-fn', type=str, help='Search with full-name')
    parser.add_argument('-ip', type=str, help='Search with ip address')
    parser.add_argument('-u', type=str, help='Search with username')

    args = parser.parse_args()

    if args.fn or args.ip or args.u:
        if args.fn:
            result = search_full_name(args.fn)
            print("\n\n", result)
            save_result_to_file(result)
        elif args.ip:
            result = search_ip_address(args.ip)
            print("\n\n", result)
            save_result_to_file(result)
        elif args.u:
            result = search_username(args.u.lstrip('@'))
            print("\n\n", result)
            save_result_to_file(result)
    else:
        print("Démarrage de l'API...")

        flask_thread = Thread(target=run_flask)
        flask_thread.start()

if __name__ == "__main__":
    main()

