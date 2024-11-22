import pyvisa
import socks
import socket

# Configura il proxy SOCKS
socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
socket.socket = socks.socksocket

# Crea un ResourceManager
rm = pyvisa.ResourceManager()

# Specifica l'indirizzo del dispositivo TCP/IP
instrument = rm.open_resource('TCPIP0::192.168.1.198::inst0::INSTR')

# Esegui un comando di identificazione
print(instrument.query('*IDN?'))
