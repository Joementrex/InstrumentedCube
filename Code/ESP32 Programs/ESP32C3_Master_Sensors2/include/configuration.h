// Header file for the configuration of instruments and sensors 
#include <Arduino.h>

// ------- WIFI Configuration Definitions ---------
// ENTER THE WIFI MAC ADDRESS OF THE RECIEVER HERE
uint8_t receiverMAC[] = {0x34, 0x85, 0x18, 0x02, 0xFB, 0x3D};

// Using multiplexer 
#define USE_MULTIPLEXER 1

// ------- MCP23017 Configuration Definitions ---------
// MCP23017 I2C address is 0x20(32)
Adafruit_MCP23X17 mcp;
// Store the pin number for A0 to A7 
const int PinA0 = 0;
const int PinA1 = 1;
const int PinA2 = 2;
const int PinA3 = 3;
const int PinA4 = 4;
const int PinA5 = 5;
const int PinA6 = 6;
const int PinA7 = 7;
// Store the pin number for B0 to B7
const int PinB0 = 8;
const int PinB1 = 9;
const int PinB2 = 10;
const int PinB3 = 11;
const int PinB4 = 12;
const int PinB5 = 13;
const int PinB6 = 14;
const int PinB7 = 15;

// ------- TMAG Sensor Configuration Definitions ---------

//Config Values to be Used 
#define SET_DEVICE_CONFIG_1_REGFIELD 0x10  // 0b00010000 - 16x average sampling, default is 0x00 = 1x averag
#define SET_DEVICE_CONFIG_2_REGFIELD 0x02  // 0b00000010 - continuous measure mode
#define SET_SENSOR_CONFIG_1_REGFIELD 0x74  // 0b01110100 - First 4 bits for enabling X, Y & Z magnetic channels & next 4 bits (to LSB) setting sleep time to 20mS.

//Sensitivity
#define SET_SENSOR_CONFIG_2_REGFIELD 0x04  // 0b00000100 - X, Y and Z range set to default (A1 = 40mT, A2 =133mT), angle channel X & Y enabled.
//#define SET_SENSOR_CONFIG_2_REGFIELD 0x07  // 0b00000111 - X, Y and Z range set to (A1 = 80mT, A2 =266mT), angle channel X & Y enabled.

// register list.

// Register Addresses
#define REG_DEVICE_CONFIG_1 0x00
#define REG_DEVICE_CONFIG_2 0x01
#define REG_SENSOR_CONFIG_1 0x02
#define REG_SENSOR_CONFIG_2 0x03
#define REG_X_THR_CONFIG 0x04
#define REG_Y_THR_CONFIG 0x05
#define REG_Z_THR_CONFIG 0x06
#define REG_T_CONFIG 0x07
#define REG_INT_CONFIG_1 0x08
#define REG_MAG_GAIN_CONFIG 0x09
#define REG_MAG_OFFSET_CONFIG_1 0x0A
#define REG_MAG_OFFSET_CONFIG_2 0x0B
#define REG_I2C_ADDRESS 0x0C
#define REG_DEVICE_ID 0x0D
#define REG_MANUFACTURER_ID_LSB 0x0E
#define REG_MANUFACTURER_ID_MSB 0x0F
#define REG_T_MSB_RESULT 0x10
#define REG_T_LSB_RESULT 0x11
#define REG_X_MSB_RESULT 0x12
#define REG_X_LSB_RESULT 0x13
#define REG_Y_MSB_RESULT 0x14
#define REG_Y_LSB_RESULT 0x15
#define REG_Z_MSB_RESULT 0x16
#define REG_Z_LSB_RESULT 0x17
#define REG_CONV_STATUS 0x18
#define REG_ANGLE_RESULT_MSB 0x19
#define REG_ANGLE_RESULT_LSB 0x1A
#define REG_MAGNITUDE_RESULT 0x1B
#define REG_DEVICE_STATUS 0x1C

//calculation values.

#define TEMP_SENS_T0 25.0
#define TEMP_ADC_T0 17508
#define TEMP_ADC_RESOLUTION 60.1
#define ANGLE_RESOLUTION 16.0
#define XYZ_SENSITIVITY_40mT 820.0
#define XYZ_SENSITIVITY_80mT 410.0

//Device Addresses: refer to 8.2.2 (I2C Address Expansion) of the TMAG5273 datasheet fr configuration

#define General_CALL_ADDRESS 0x00  //0's in forst 8 bits to address multiple i2c devices.
#define I2C_ADDRESS_RESET 0x6A


#define TMAG5273_DEVICE_ADDRESS 0x35

// Define array of addresses for the TMAG5273 devices
const uint8_t TMAG5273_DEVICE_ADDRESSES[] = {0x35, 0x36, 0x37, 0x38, 0x39, 0x3A,
                                             0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40,
                                             0x41, 0x42, 0x43, 0x44, 0x45};

#define DEVICE_1_ADDRESS 0x35
#define Device_1_Write_ADDRESS 0x6A
#define Device_1_Read_ADDRESS 0x6B

#define NEW_DEVICE_2_ADDRESS 0x23  //0b100011
#define DEVICE_2_ADDRESS 0x22      //0b100010
//#define Device_2_Write_ADDRESS 0x44
//#define Device_2_Read_ADDRESS 0x45

#define NEW_DEVICE_3_ADDRESS 0x79
#define DEVICE_3_ADDRESS 0x78
//#define Device_3_Write_ADDRESS 0xF0
//#define Device_3_Read_ADDRESS 0xF1

#define NEW_DEVICE_4_ADDRESS 0x45
#define DEVICE_4_ADDRESS 0x44
//#define Device_4_Write_ADDRESS 0x88
//#define Device_4_Read_ADDRESS 0x89

#define NEW_DEVICE_5_ADDRESS 0x4B
#define DEVICE_5_ADDRESS 0x4A

#define NEW_DEVICE_6_ADDRESS 0x51
#define DEVICE_6_ADDRESS 0x50

#define NEW_DEVICE_7_ADDRESS 0x57
#define DEVICE_7_ADDRESS 0x56

#define NEW_DEVICE_8_ADDRESS 0x5D
#define NEW_DEVICE_9_ADDRESS 0x63
// Do not go above i2c 127, go from 0x63 and count up by one
#define NEW_DEVICE_10_ADDRESS 0x64
#define NEW_DEVICE_11_ADDRESS 0x65
#define NEW_DEVICE_12_ADDRESS 0x66
#define NEW_DEVICE_13_ADDRESS 0x67
#define NEW_DEVICE_14_ADDRESS 0x68
#define NEW_DEVICE_15_ADDRESS 0x69
#define NEW_DEVICE_16_ADDRESS 0x6A


//DEFAULT Config VALUES

#define DEVICE_CONFIG_1_REGFIELD 0x00      // set to default
#define DEVICE_CONFIG_2_REGFIELD 0x00      // set to default
#define SENSOR_CONFIG_1_REGFIELD 0x74      // 0b01110100 - First 4 bits for enabling X, Y & Z magnetic channels & next 4 bits (to LSB) setting sleep time to 20mS.
#define SENSOR_CONFIG_2_REGFIELD 0x04      // 0b00000100 - X, Y and Z range set to default (A1 = 40mT, A2 =133mT), angle channel X & Y enabled.
#define X_THR_CONFIG_REGFIELD 0x00         // set to default
#define Y_THR_CONFIG_REGFIELD 0x00         // set to default
#define Z_THR_CONFIG_REGFIELD 0x00         // set to default
#define T_CONFIG_REGFIELD 0x01             // 0b00000001 - Enabled data acquisition of temperature channel
#define INT_CONFIG_1_REGFIELD 0x00         // set to default
#define MAG_GAIN_CONFIG_REGFIELD 0x00      // set to default
#define MAG_OFFSET_CONFIG_1_REGFIELD 0x00  // set to default
#define MAG_OFFSET_CONFIG_2_REGFIELD 0x00  // set to default