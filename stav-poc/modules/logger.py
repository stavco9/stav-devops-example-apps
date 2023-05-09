import os
import sys
import logging
import config

class Logger():
  def __init__(self):
    self.logger = logging.getLogger()
    log_formatter = logging.Formatter(fmt='%(levelname)s — %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    self.logger.addHandler(console_handler)
    self.logger.setLevel(logging.getLevelName(config.LOG_LEVEL))

  def info(self, message, *args):
    self.logger.info(message, *args)

  def warn(self, message, *args):
    self.logger.warn(message, *args)

  def error(self, message, *args):
     self.logger.error(message, *args)

  def debug(self, message, *args):
    self.logger.debug(message, *args)