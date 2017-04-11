import socket
import logging
import datetime
from uuid import getnode as get_mac

def get_local_mac_address():
  return ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))

def get_local_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
  return s.getsockname()[0]

def get_logger(log_name):
  formatter = logging.Formatter('{0}: %(message)s'.format(datetime.datetime.utcnow()))
  logger = logging.getLogger(log_name)
  handler = logging.FileHandler('client/logs/{0}.log'.format(log_name))
  handler.setFormatter(formatter)
  logger.setLevel(logging.INFO)
  logger.addHandler(handler)
  return logger
