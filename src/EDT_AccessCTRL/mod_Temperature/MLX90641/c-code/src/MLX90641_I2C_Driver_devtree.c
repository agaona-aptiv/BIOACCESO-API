#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include "../inc/i2c.h"
#include "../inc/MLX90641_I2C_Driver.h"

I2CDevice device;

void MLX90641_I2CInit(void)
{
    int bus;
    if ((bus = i2c_open("/dev/i2c-8"))==-1){
        //return 1;
    }
    else{
        memset(&device, 0, sizeof(device));

        device.bus = bus;       // Bus 1
        device.addr = 0x33;     // Slave address is 0x33, 7bit
        device.iaddr_bytes = 2;  // Device internal addres = 2 bytes
        device.page_bytes = 16;  // Device are capable of 16 bytes per page 
        //return 0;
    } 
}

void MLX90641_I2CClose(void)
{
    int bus;
    bus = device.bus;
    i2c_close(bus);
}

int MLX90641_I2CRead(uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data)
{
    unsigned char buffer[1664];
    memset(buffer, 0, sizeof(buffer));
    uint16_t *p;
    int i=0;
    
    p=data;

    i2c_ioctl_read(&device, startAddr, buffer, 2*nMemAddressRead);


    
    for (int cnt=0; cnt<nMemAddressRead; cnt++){
        i = cnt <<1;
        *p++=(uint16_t)buffer[i]*256 +(uint16_t)buffer[i+1];
    }
    return 0;
}

void MLX90641_I2CFreqSet(int freq)
{
}

int MLX90641_I2CGeneralReset(void)
{
    return 0;
}

int MLX90641_I2CWrite(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
    unsigned char buffer[4];
    memset(buffer, 0, sizeof(buffer));
    
    buffer[0]=(char)((data>>8)&0x00FF);
    buffer[1]=(char)(data&0x00FF);

    i2c_ioctl_write(&device, writeAddress, buffer, 4);

    return 0;
}
