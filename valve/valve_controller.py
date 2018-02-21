#!/usr/bin/env python
#-*- coding: utf-8 -*-

# BBG driver firmware for the FESTO airflow valve block


from pymodbus.client.sync import ModbusTcpClient
import zmq

subAddr = 'tcp://*:1555'
valveAddr = ['10.42.0.254', '10.42.0.252']
commandRegAddr = [40003, 40004, 40005, 40006]

festoValveBlocks = []
for valve in valveAddr:
    festoValveBlocks.append(ModbusTcpClient(valve))

#disable modbus connection timeout for cpx fb36
#returnvalue = festoValveBlocks[1].write_register(46100, 0)

zmqContext = zmq.Context(1)
zmqSub = zmqContext.socket(zmq.SUB)
zmqSub.bind(subAddr)
zmqSub.setsockopt(zmq.SUBSCRIBE, '')

# initialize valve states
valveStates = [[0, 0, 0, 0], [0, 0, 0, 0]];

for iBlock in range(0,2):
    for i in range(0, 4):
        festoValveBlocks[iBlock].write_register(commandRegAddr[i], valveStates[iBlock][i])

command2state = {'On': 1, 'Off': 0}

zmqSub.RCVTIMEO = 1000

print "Start"

while 1:
    try:
        # receive valve message
        [name, device, command, data] = zmqSub.recv_multipart()
        # get referenced valve number
        valve = int(name[-3:])

        # Map all names to the 1-32 range, choose valve block
        if valve > 32:
            valve -= 32
            iBlock = 1
        else:
            iBlock = 0
        # get valve address byte and number in byte
        [byteIdx, valveIdx] = divmod(valve-1, 8)
        valveIdx = valveIdx + 1

        # check valve state ("on" or "off")
        if command2state[command] :

            # set valve bit to "1"
            valveStates[iBlock][byteIdx] = valveStates[iBlock][byteIdx] | (1 << (valveIdx-1))
        else:
            # set valve bit to "0"
            valveStates[iBlock][byteIdx] = valveStates[iBlock][byteIdx] & ~(1 << (valveIdx-1))
        # send demanded valve states to FESTO valve block
        returnvalue = festoValveBlocks[iBlock].write_register(commandRegAddr[byteIdx], valveStates[iBlock][byteIdx])
    except KeyboardInterrupt:
        print "Interrupt received. Exiting..."
        raise
    except:
        for iBlock in [0, 1]:
            response = festoValveBlocks[iBlock].read_holding_registers(commandRegAddr[0], 4)


