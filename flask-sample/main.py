import os
from flask import Flask, session, request
from modules.prometheus_metrics import PrometheusClient
from modules.logger import Logger
import config
app = Flask(__name__)

logger = Logger()
logger.info(f"microservice: {config.MICROSERVICE} | environment: {config.ENVIRONMENT} | log level: {config.LOG_LEVEL}")

prom = PrometheusClient()
 
@app.route('/')
def root_url():
    return hello_world()

@app.route('/hello')
def hello_world():
    return "<h1>Hello world</h1>"

@app.route('/metrics')
def metrics_sample():
    return prom.metrics()

@app.route('/inc')
def increase_session():
    prom.increase_counter()

    return f"Session counter is {prom.get_counter()}"

@app.route('/dec')
def decrease_session():
    prom.decrease_counter()

    return f"Session counter is {prom.get_counter()}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("LISTEN_PORT") or 3000)