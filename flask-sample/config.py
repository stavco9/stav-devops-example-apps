import os

LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"
ENVIRONMENT = os.getenv("ENVIRONMENT") or "DEV"
MICROSERVICE = os.getenv("MICROSERVICE") or "stav-poc"