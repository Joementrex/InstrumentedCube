#include <Arduino.h>
#include <Wire.h>
#include <HardwareSerial.h>
HardwareSerial MySerial0(0);

// test of errors import wifi headers
#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h> // only for esp_wifi_set_channel()

// ------------------ ESP-NOW Configuration ------------------
// Global copy of slave
esp_now_peer_info_t slave;
#define CHANNEL 1
#define PRINTSCANRESULTS 0
#define DELETEBEFOREPAIR 0


//USER CONFIGURATIONS

int samplingMode = 0;  //grabs 500 samples upon user input of position as an int

int rawMode = 1;  //spits out raw XYZ data

int timedSamplingMode = 0;  //grabs 500 samples, waits 3s, then repeats as many times as defined in the for loop.

//multi sensor parameters
int sensor1 = D8;
int sensor2 = D0;
int sensor3 = D10;


//Config Values to be Used

#define SET_DEVICE_CONFIG_1_REGFIELD 0x10  // 0b00010000 - 16x average sampling, default is 0x00 = 1x averag
#define SET_DEVICE_CONFIG_2_REGFIELD 0x02  // 0b00000010 - continuous measure mode
#define SET_SENSOR_CONFIG_1_REGFIELD 0x74  // 0b01110100 - First 4 bits for enabling X, Y & Z magnetic channels & next 4 bits (to LSB) setting sleep time to 20mS.

//Sensitivity
#define SET_SENSOR_CONFIG_2_REGFIELD 0x04  // 0b00000100 - X, Y and Z range set to default (A1 = 40mT, A2 =133mT), angle channel X & Y enabled.
//#define SET_SENSOR_CONFIG_2_REGFIELD 0x07  // 0b00000111 - X, Y and Z range set to (A1 = 80mT, A2 =266mT), angle channel X & Y enabled.

// register list.

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


int nDevices;
int deviceAddresses[6];

void IIC_Write(int8_t deviceAddress, int8_t registerAddress, int8_t dataToWrite) {
  Wire.beginTransmission(deviceAddress);
  Wire.write(registerAddress);
  Wire.write(dataToWrite);
  Wire.endTransmission(1);
}

void configureDevice() {

  if (nDevices == 0) {
    //Serial.println("setOperatingMode: No Devices Detected");
  } else if (nDevices == 1) {
    //Serial.println("Configuring device\n");
    IIC_Write(deviceAddresses[1], REG_DEVICE_CONFIG_1, DEVICE_CONFIG_1_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_DEVICE_CONFIG_2, DEVICE_CONFIG_2_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_SENSOR_CONFIG_1, SENSOR_CONFIG_1_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_SENSOR_CONFIG_2, SENSOR_CONFIG_2_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_X_THR_CONFIG, X_THR_CONFIG_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_Y_THR_CONFIG, Y_THR_CONFIG_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_Z_THR_CONFIG, Z_THR_CONFIG_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_T_CONFIG, T_CONFIG_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_INT_CONFIG_1, INT_CONFIG_1_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_MAG_GAIN_CONFIG, MAG_GAIN_CONFIG_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_MAG_OFFSET_CONFIG_1, MAG_OFFSET_CONFIG_1_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_MAG_OFFSET_CONFIG_2, MAG_OFFSET_CONFIG_2_REGFIELD);
    //Serial.println("done\n");
  } else {
    for (int i = 1; i <= nDevices; i++) {
      //Serial.print("Configuring device ");
      //Serial.println(i);
      IIC_Write(deviceAddresses[i], REG_DEVICE_CONFIG_1, DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_DEVICE_CONFIG_2, DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_SENSOR_CONFIG_1, SENSOR_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_SENSOR_CONFIG_2, SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_X_THR_CONFIG, X_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_Y_THR_CONFIG, Y_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_Z_THR_CONFIG, Z_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_T_CONFIG, T_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_INT_CONFIG_1, INT_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_MAG_GAIN_CONFIG, MAG_GAIN_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_MAG_OFFSET_CONFIG_1, MAG_OFFSET_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_MAG_OFFSET_CONFIG_2, MAG_OFFSET_CONFIG_2_REGFIELD);
      //Serial.println("done\n");
      /*Serial.println("Configuring device 2 \n");
      IIC_Write(deviceAddresses[2], REG_DEVICE_CONFIG_1, DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_DEVICE_CONFIG_2, DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_SENSOR_CONFIG_1, SENSOR_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_SENSOR_CONFIG_2, SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_X_THR_CONFIG, X_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_Y_THR_CONFIG, Y_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_Z_THR_CONFIG, Z_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_T_CONFIG, T_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_INT_CONFIG_1, INT_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_MAG_GAIN_CONFIG, MAG_GAIN_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_MAG_OFFSET_CONFIG_1, MAG_OFFSET_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_MAG_OFFSET_CONFIG_2, MAG_OFFSET_CONFIG_2_REGFIELD);
      Serial.println("done\n");
      Serial.println("Configuring device 3 \n");
      IIC_Write(deviceAddresses[3], REG_DEVICE_CONFIG_1, DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_DEVICE_CONFIG_2, DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_SENSOR_CONFIG_1, SENSOR_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_SENSOR_CONFIG_2, SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_X_THR_CONFIG, X_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_Y_THR_CONFIG, Y_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_Z_THR_CONFIG, Z_THR_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_T_CONFIG, T_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_INT_CONFIG_1, INT_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_MAG_GAIN_CONFIG, MAG_GAIN_CONFIG_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_MAG_OFFSET_CONFIG_1, MAG_OFFSET_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_MAG_OFFSET_CONFIG_2, MAG_OFFSET_CONFIG_2_REGFIELD);
      Serial.println("done\n");*/
    }
  }
}

void setOperatingMode() {
  if (nDevices == 0) {
    //Serial.println("setOperatingMode: No Devices Detected");
  } else if (nDevices == 1) {
    //Serial.println("setting operating mode\n");
    IIC_Write(deviceAddresses[1], REG_DEVICE_CONFIG_2, SET_DEVICE_CONFIG_2_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_DEVICE_CONFIG_1, SET_DEVICE_CONFIG_1_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_SENSOR_CONFIG_2, SET_SENSOR_CONFIG_2_REGFIELD);
    IIC_Write(deviceAddresses[1], REG_SENSOR_CONFIG_1, SET_SENSOR_CONFIG_1_REGFIELD);
    //Serial.println("done\n");
  } else {
    for (int i = 1; i <= nDevices; i++) {

      //Serial.print("setting operating mode of device ");
      //Serial.println(i);
      IIC_Write(deviceAddresses[i], REG_DEVICE_CONFIG_2, SET_DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_DEVICE_CONFIG_1, SET_DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_SENSOR_CONFIG_2, SET_SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[i], REG_SENSOR_CONFIG_1, SET_SENSOR_CONFIG_1_REGFIELD);
      //Serial.println("done\n");
      /*Serial.println("setting operating mode of device 3 \n");
      IIC_Write(deviceAddresses[2], REG_DEVICE_CONFIG_2, SET_DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_DEVICE_CONFIG_1, SET_DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_SENSOR_CONFIG_2, SET_SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[2], REG_SENSOR_CONFIG_1, SET_SENSOR_CONFIG_1_REGFIELD);
      Serial.println("setting operating mode of device 4 \n");
      IIC_Write(deviceAddresses[3], REG_DEVICE_CONFIG_2, SET_DEVICE_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_DEVICE_CONFIG_1, SET_DEVICE_CONFIG_1_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_SENSOR_CONFIG_2, SET_SENSOR_CONFIG_2_REGFIELD);
      IIC_Write(deviceAddresses[3], REG_SENSOR_CONFIG_1, SET_SENSOR_CONFIG_1_REGFIELD);
      */
    }
  }
}

void readXYZData() {
  if (nDevices == 0) {
    //Serial.println("setOperatingMode: No Devices Detected");
  } else if (nDevices == 1) {
    Wire.beginTransmission(deviceAddresses[1]);  // transmit to device address
    Wire.write(REG_X_MSB_RESULT);                // sends register address
    Wire.endTransmission(1);                     // stop transmitting
    Wire.requestFrom(deviceAddresses[1], 7);     // Ask for 7 bytes, once done, bus is released by default
    byte X_MSB = Wire.read();
    byte X_LSB = Wire.read();
    byte Y_MSB = Wire.read();
    byte Y_LSB = Wire.read();
    byte Z_MSB = Wire.read();
    byte Z_LSB = Wire.read();
    byte DEV_CONF = Wire.read();
    int16_t X_RESULT = ((X_MSB << 8) | X_LSB);  // 16bits that make up the X channel data
    int16_t Y_RESULT = ((Y_MSB << 8) | Y_LSB);  // 16bits that make up the Y channel data
    int16_t Z_RESULT = ((Z_MSB << 8) | Z_LSB);  // 16bits that make up the Z channel data

    //Serial.print(X_RESULT);
    //Serial.print(",");
    //Serial.print(Y_RESULT);
    //Serial.print(",");
    //Serial.println(Z_RESULT);
  } else {
    for (int i = 1; i <= nDevices; i++) {
      Wire.beginTransmission(deviceAddresses[i]);  // transmit to device address
      Wire.write(REG_X_MSB_RESULT);                // sends register address
      Wire.endTransmission(1);                     // stop transmitting
      Wire.requestFrom(deviceAddresses[i], 7);     // Ask for 7 bytes, once done, bus is released by default
      byte X_MSB = Wire.read();
      byte X_LSB = Wire.read();
      byte Y_MSB = Wire.read();
      byte Y_LSB = Wire.read();
      byte Z_MSB = Wire.read();
      byte Z_LSB = Wire.read();
      byte DEV_CONF = Wire.read();
      int16_t X_RESULT = ((X_MSB << 8) | X_LSB);  // 16bits that make up the X channel data
      int16_t Y_RESULT = ((Y_MSB << 8) | Y_LSB);  // 16bits that make up the Y channel data
      int16_t Z_RESULT = ((Z_MSB << 8) | Z_LSB);  // 16bits that make up the Z channel data

      Serial.print(X_RESULT);
      MySerial0.print(X_RESULT);
      Serial.print(",");
      MySerial0.print(",");
      Serial.print(Y_RESULT);
      MySerial0.print(Y_RESULT);
      Serial.print(",");
      MySerial0.print(",");
      Serial.print(Z_RESULT);
      MySerial0.print(Z_RESULT);
      if (i != nDevices) {
        Serial.print(",");
        MySerial0.print(",");
      }
    }
    Serial.println();
    MySerial0.println();
  }
}



void reset_Addresses() {}


void assign_Addresses() {
  //I2C_ADDRESS Register (Offset = Ch) [Reset = 6Ah]
  //7-bit default factory I2C address is loaded from OTP during first
  //power up. Change these bits to a new setting if a new I2C address
  //is required (at each power cycle these bits must

  digitalWrite(sensor1, HIGH);
  digitalWrite(sensor2, HIGH);
  digitalWrite(sensor3, HIGH);
  delay(10);
  IIC_Write(General_CALL_ADDRESS, REG_I2C_ADDRESS, I2C_ADDRESS_RESET);
  delay(10);


  digitalWrite(sensor1, HIGH);
  digitalWrite(sensor2, LOW);
  digitalWrite(sensor3, LOW);
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_2_ADDRESS);
  delay(10);

  digitalWrite(sensor1, HIGH);
  digitalWrite(sensor2, HIGH);
  digitalWrite(sensor3, LOW);
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_3_ADDRESS);
  delay(10);

  digitalWrite(sensor1, HIGH);
  digitalWrite(sensor2, HIGH);
  digitalWrite(sensor3, HIGH);
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_4_ADDRESS);
  delay(10);
}


void setup() {
  Serial.begin(115200);  // start serial for output
  MySerial0.begin(115200, SERIAL_8N1, -1, -1);
  Serial.println("GPIO SET UP...");
  MySerial0.println("GPIO SET UP...");


  Wire.begin();  // join i2c bus with address #4


  //pinMode(4, INPUT_PULLUP); //SDA internal pull up
  //pinMode(5, INPUT_PULLUP); //SCL internal pull up

  byte error, address;

  pinMode(sensor1, OUTPUT);
  pinMode(sensor2, OUTPUT);
  pinMode(sensor3, OUTPUT);


  digitalWrite(sensor1, LOW);
  digitalWrite(sensor2, LOW);
  digitalWrite(sensor3, LOW);

  assign_Addresses();

  digitalWrite(sensor1, HIGH);
  digitalWrite(sensor2, HIGH);
  digitalWrite(sensor3, HIGH);



  Serial.println("Scanning...");
  MySerial0.println("Scanning...");


  nDevices = 0;

  for (address = 1; address < 127; address++) {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      //Serial.print("I2C device found at address 0x");
      MySerial0.print("I2C device found at address 0x");
      if (address < 16) {

        //Serial.print("0");
        MySerial0.print("0");
      }
      //Serial.print(address, HEX);
      MySerial0.print(address, HEX);
      //Serial.println("  !");
      MySerial0.println("  !");

      nDevices++;
      deviceAddresses[nDevices] = address;

    } else if (error == 4) {
      //Serial.print("Unknown error at address 0x");
      MySerial0.print("Unknown error at address 0x");
      if (address < 16) {
        //Serial.print("0");
        MySerial0.print("0");
      }

      //Serial.println(address, HEX);
      MySerial0.println(address, HEX);
    }
  }
  if (nDevices == 0) {
    //Serial.println("No I2C devices found\n");
    MySerial0.println("No I2C devices found\n");
  } else {
    //Serial.println("done\n");
    MySerial0.println("done\n");
  }



  configureDevice();
  setOperatingMode();
}


int pos = 0;
void loop() {
  if (samplingMode == 1) {
    while (Serial.available() == 0) {
    }
    int userInput = Serial.parseInt();
    if (userInput > 0) {
      for (int samples = 0; samples <= 1000; samples++) {
        //Serial.print(userInput);
        //Serial.print(",");
        readXYZData();
        delay(1);
      }
    }
  } else if (rawMode == 1) {
    readXYZData();
    delay(1);


  } else if (timedSamplingMode == 1) {
    delay(5000);
    while (pos < 28) {
      for (int samples = 0; samples <= 500; samples++) {
        //Serial.print(String(pos) + ",");
        MySerial0.print(String(pos) + ",");
        readXYZData();
        delay(1);
      }
      delay(3000);
      pos++;
    }
  }
}