import pymodbus
import logging
import json
import getmac
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.register_read_message import ReadInputRegistersResponse
#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate = '9600', timeout=0.3)
#connection = client.connect()
#print(connection)
from pymodbus.version import version
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartTlsServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
from custom_message import CustomModbusRequest
from getmac import get_mac_address as gma

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
exceptionJson = [0]*100
GMA = gma()
def run_server():
	
    try json_file = open("data.json", "r")
	data = json.load(json_file)
	data_array = data['data_array']
    except:
	data_array = exceptionJson
    
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, data_array),
        ir=ModbusSequentialDataBlock(0, [0]*100))

    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()

    # TCP Server

    StartTcpServer(context, identity=None, address=("169.254.70.96", 5020))
#"localhost", 5020),
    # TCP Server with deferred reactor run

    # from twisted.internet import reactor
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                defer_reactor_run=True)
    # reactor.run()

    # Server with RTU framer
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                framer=ModbusRtuFramer)

    # RTU Server
    # StartSerialServer(context, identity=identity,
    #                   port='/dev/ttyp0', framer=ModbusRtuFramer)

    exceptionJson = data_array
    with open("data.json", "w") as outfile:
	json.dump(data, outfile)

#if __name__ == "__main__":
while True:
    run_server()


#def ficar_rodando():
        #value = client.read_holding_registers(0, 1, unit=0x01)
        #print(value.registers[0])
        #oi = value.registers[0]


#while True:
#       ficar_rodando()


