# python snmp trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import logging
from datetime import date
import os

snmpEngine = engine.SnmpEngine()

Port = 162  # trap listener port
TrapAgentAddress = '10.0.3.15'  # Trap listener address

# Checks if log file exist
if not os.path.isfile(f'./received_traps_{date.today().year}_{date.today().month}_{date.today().day}.log'):
    print('New file created!')
    # Creates a new log file for the current day
    with open(f'received_traps_{str(date.today().year)}_{str(date.today().month)}_{str(date.today().day)}.log', 'w') as f:
        f.write('Create a new text file!')

logging.basicConfig(filename=f'received_traps_{date.today().year}_{date.today().month}_{date.today().day}.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info(f'Agent is listening SNMP Trap on {TrapAgentAddress} , Port : {str(Port)}')
logging.info('--------------------------------------------------------------------------\n')

print(f'Agent is listening SNMP Trap on {TrapAgentAddress} , Port : {str(Port)}')

config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
)

# Configure community here
config.addV1System(snmpEngine, 'my-area', 'public')


def terminal_output(snmpEngine, stateReference, contextEngineId, contextName, varbinds, cbCtx):
    print('Received new Trap message')
    logging.info('Received new Trap message')
    for name, val in varbinds:
        logging.info('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

    logging.info('==== End of Incoming Trap ====\n')


ntfrcv.NotificationReceiver(snmpEngine, terminal_output)

snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except ValueError:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
