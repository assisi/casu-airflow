########################################################
#########   valve controller BB firmware   #############
#########         created: 11/30/15        #############
#########            D.M. LARICS           #############
######################################################## 


from pymodbus.client.sync import ModbusTcpClient
import zmq

subAddr = 'tcp://*:1555'
valveAddr = '10.42.0.254'
commandRegAddr = 40003


festoValveBlock = ModbusTcpClient(valveAddr)
zmqContext = zmq.Context(1)
zmqSub = zmqContext.socket(zmq.SUB)
zmqSub.bind(subAddr)
zmqSub.setsockopt(zmq.SUBSCRIBE, '')

# initialize valve states
valveStates = 0;
festoValveBlock.write_register(commandRegAddr, valveStates)

command2state = {'On': 1, 'Off': 0}

while 1:
	# receive valve message
	[name, device, command, data] = zmqSub.recv_multipart()
	
	# get referenced valve number
	valve = int(name[-3:])
	
	# check valve state ("on" or "off")
	if command2state[command] :

		# set valve bit to "1"
		valveStates = valveStates | (1 << (valve-1))

	else:

		# set valve bit to "0"
		valveStates = valveStates & ~(1 << (valve-1))

	# send demanded valve states to FESTO valve block
	festoValveBlock.write_register(commandRegAddr, valveStates)



