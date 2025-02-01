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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)