# Jaesung Choi (jc13152)
from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if all parameters are provided
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request", 400

    # Query the authoritative server for IP
    ip = query_authoritative_server(hostname, as_ip, as_port)

    if not ip:
        return "Failed to retrieve IP from AS", 500

    # Make a request to the Fibonacci server
    try:
        response = requests.get(f"http://{ip}:{fs_port}/fibonacci?number={number}")
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        return str(e), 500

def query_authoritative_server(hostname, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

    response, _ = sock.recvfrom(1024)
    lines = response.decode().split("\n")
    for line in lines:
        if line.startswith("VALUE="):
            return line.split("=")[1]
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)