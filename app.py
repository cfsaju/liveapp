import os
import socket
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['endpoint'])

@app.route('/')
def home():
    REQUEST_COUNT.labels(endpoint='/').inc()
    return jsonify({"message": "OK", "status": 200}), 200

@app.route('/fail')
def fail():
    REQUEST_COUNT.labels(endpoint='/fail').inc()
    return jsonify({"message": "Internal Server Error", "status": 500}), 500

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

@app.route('/healthz')  # Liveness probe
@app.route('/readyz')   # Readiness probe
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info')  #To print pod name and IP
def info():
    pod_name = os.getenv('HOSTNAME', 'Unknown')
    try:
        pod_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        pod_ip = "Unable to determine IP"
    
    return jsonify({"pod_name": pod_name, "pod_ip": pod_ip}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
