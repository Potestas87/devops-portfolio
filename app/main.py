import os
import time

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])

VERSION = os.getenv("APP_VERSION", "dev")


@app.before_request
def start_timer():
    request._start = time.perf_counter()


@app.after_request
def record_metrics(response):
    path = request.url_rule.rule if request.url_rule else "unmatched"
    LATENCY.labels(path).observe(time.perf_counter() - request._start)
    REQUESTS.labels(request.method, path, response.status_code).inc()
    return response


@app.get("/")
def index():
    return jsonify(service="api", version=VERSION)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/fail")
def fail():
    """Deliberate 500 so alerts and dashboards can be demonstrated."""
    return jsonify(error="simulated failure"), 500


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
