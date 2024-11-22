import pyvisa
import socks
import socket

# Configura il proxy SOCKS
# "ssh-socks-proxy" e' il nomedel container, altrimenti dovresti usare localhost
socks.set_default_proxy(socks.SOCKS5, "ssh-socks-proxy", 1080)
socket.socket = socks.socksocket

# Crea un ResourceManager
rm = pyvisa.ResourceManager()

# Specifica l'indirizzo del dispositivo TCP/IP
instrument = rm.open_resource('TCPIP0::192.168.1.198::inst0::INSTR')

# Esegui un comando di identificazione
print(instrument.query('*IDN?'))
