# Jaesung Choi (jc13152)
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    # Register with the authoritative server
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

    return "Registered successfully", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        n = int(number)
    except ValueError:
        return "Bad format", 400

    result = fib(n)
    return jsonify({"fibonacci": result}), 200

def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)