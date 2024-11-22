import pyvisa

# Crea un ResourceManager
rm = pyvisa.ResourceManager()

# Specifica l'indirizzo del dispositivo TCP/IP
instrument = rm.open_resource('TCPIP0::localhost::INSTR')

# Esegui un comando di identificazione
print(instrument.query('*IDN?'))
