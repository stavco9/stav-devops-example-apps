import prometheus_client as prom
from modules.logger import Logger

class PrometheusClient:
  def __init__(self):
    self.counter_metric = prom.Gauge('sessions_counter', "This is a session counter metric")
    self.logger = Logger()

  def increase_counter(self):
    self.counter_metric.inc()
    self.logger.info(f"Increased counter to {self.counter_metric._value.get()}")

  def decrease_counter(self):
    if self.counter_metric._value.get() > 0:
      self.counter_metric.dec()
      self.logger.info(f"Decrease counter to {self.counter_metric._value.get()}")

  def get_counter(self):
    return self.counter_metric._value.get()

  def metrics(self):
    return prom.generate_latest()
    