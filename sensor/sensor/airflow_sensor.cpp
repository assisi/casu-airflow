/*! \file  mainApp.cpp
    \brief Example of CASU_Interface class usage.
 */

#include "i2cSlaveMCU.h"

#include <stdio.h>
#include <unistd.h>
#include <math.h>

using namespace std;


int main(int argc, char **argv) {
	int sensorSerialNumH = 0xA734;
	int sensorSerialNumL = 0x5EFE;
	I2C_SlaveMCU i2cPIC;
	char inBuff[2] = {0};
	int i2c_bus = 2, sensorAddress = 73, inData = 0;

	i2cPIC.initI2C(i2c_bus, sensorAddress);

    printf("Starting airflow measurement...");
	while (1)	{
		i2cPIC.receiveData(inBuff, 2);
		inData = (inBuff[0]<<8) + inBuff[1];

		if (inData!=0x0000 && inData!=sensorSerialNumH && inData!=sensorSerialNumL)  {
			printf("Flow: %0.3f SLPM\n\n", roundf(50.0*(((float) inData / 16384.0)-0.1) / 0.8*10) /10);
			//printf("Flow: %0.3f SLPM\n", 50.0*(((float) inData / 16384.0)-0.1) / 0.8*10);
		}
        else
        {
            printf("Corrupt data packet received!")
        }
		sleep(3);
		
	}

	return 0;
}
