import json
import socket
import time

from . import utils, constants

server_address = (constants.SOCKET_SERVER_IP, constants.SOCKET_SERVER_PORT)

logger            = utils.get_logger('client_ping_record')
logger2           = utils.get_logger('connection_fail_record')
local_mac_address = utils.get_local_mac_address()
local_ip_address  = utils.get_local_ip()

data = json.dumps( {
    "mac_address": local_mac_address,
    "ip_address": local_ip_address
  } )

# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  # Establish connection to TCP server and exchange data
  tcp_client.connect(server_address)
  tcp_client.sendall(data.encode())
  # Read data from the TCP server and close the connection
  received = tcp_client.recv(1024)

  if (received):
    if (received.decode() == 'OK'):
      print ('Conexion exitosa')
      logger.info('OK.')
    elif (received.decode() == 'DELETE'):
      print ('Terminal bloqueado')
      logger.info('EXEC DELETE.')
except ConnectionRefusedError:
  print ('Conexion rechazada')
  logger.exception('exec COMMUNICATION.')
  with open('client/logs/{0}.log'.format('connection_fail_record')) as f:
    last = None
    for line in (line for line in f if line.rstrip('\n')):
      last = line.split(':')[-1]
    last = int(last) + 1 if last else 1
    logger2.info(last)
    if(last >= 15):
      logger.info('{0} days without connection.'.format(last))      
except TimeoutError:
  print ('Tiempo de espera agotado')
finally:
  tcp_client.close()
