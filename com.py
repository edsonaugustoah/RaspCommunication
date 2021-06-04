    import pymodbus

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

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def run_server():

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [18]*100),
        co=ModbusSequentialDataBlock(0, [18]*100),
        hr=ModbusSequentialDataBlock(0, [18]*100),
        ir=ModbusSequentialDataBlock(0, [18]*100))

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

    # UDP Server
    # StartUdpServer(context, identity=identity, address=("127.0.0.1", 5020))

    # RTU Server
    # StartSerialServer(context, identity=identity,
    #                   port='/dev/ttyp0', framer=ModbusRtuFramer)

if __name__ == "__main__":
    run_server()


#def ficar_rodando():
        #value = client.read_holding_registers(0, 1, unit=0x01)
        #print(value.registers[0])
        #oi = value.registers[0]


#while True:
#       ficar_rodando()


