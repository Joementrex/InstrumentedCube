// STORED MAC ADDRESSES FOR LATER USE (THESE ARE SOFTAP MAC ADDRESSES DO NOT USE THE NORMAL MAC ADDRESSES)
// ONE IN 3D printed CUBE 34:85:18:03:DD:F9 {0x34, 0x85, 0x18, 0x03, 0xDD, 0xF9};
// EXTERNAL ONE 34:85:18:02:FB:3D {0x34, 0x85, 0x18, 0x02, 0xFB, 0x3D};


#include <Arduino.h>
#include <Wire.h>
#include <HardwareSerial.h>
// HardwareSerial //MySerial0(0);

// test of errors import wifi headers
#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h> // only for esp_wifi_set_channel()

// Header files



// ------------------ Temporary Variables for Testing ------------------
int16_t ValuesArrayZero[30] = {0};
// // Reset flag 
// volatile bool resetFlag = false;



// ------------------ ESP-NOW Configuration ------------------
// Global copy of slave
esp_now_peer_info_t slave;
#define CHANNEL 1
#define PRINTSCANRESULTS 0
#define DELETEBEFOREPAIR 0

// !!!!!!!!! This vlaue is important, defines the send packet data
// Make sure to update as more sensors are added!
#define NUM_VALUES 6
// TO DO, UPDATE TO NUMBER OF DEVICES
struct DataPacket {
  int16_t values[NUM_VALUES * 3];
};

// Recievers MAC Address
uint8_t receiverMAC[] = {0x34, 0x85, 0x18, 0x02, 0xFB, 0x3D};

// Power switch pin
// #define POWER_SWITCH_PIN 2s

// ------------------ User configuration ------------------

int samplingMode = 0;  //grabs 500 samples upon user input of position as an int

int rawMode = 1;  //spits out raw XYZ data

int timedSamplingMode = 0;  //grabs 500 samples, waits 3s, then repeats as many times as defined in the for loop.

//multi sensor parameters
int sensor1 = D8;
int sensor2 = D0;
int sensor3 = D10;


// Update this list for  6 sensors 
//  ISSUE WITH D9, DO NOT USE
int sensorPins[6] = {D0, D1, D2, D7, D8, D9};

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

#define NEW_DEVICE_5_ADDRESS 0x4B
#define DEVICE_5_ADDRESS 0x4A

#define NEW_DEVICE_6_ADDRESS 0x51
#define DEVICE_6_ADDRESS 0x50

#define NEW_DEVICE_7_ADDRESS 0x57
#define DEVICE_7_ADDRESS 0x56

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
int deviceAddresses[20];

void IIC_Write(int8_t deviceAddress, int8_t registerAddress, int8_t dataToWrite) {
  Wire.beginTransmission(deviceAddress);
  Wire.write(registerAddress);
  Wire.write(dataToWrite);
  Wire.endTransmission(1);
}

void configureDevice() {

  if (nDevices == 0) {
    Serial.println("configureDevices: No Devices Detected");
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
    Serial.println("setOperatingMode: No Devices Detected");
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

    Serial.print(X_RESULT);
    Serial.print(",");
    Serial.print(Y_RESULT);
    Serial.print(",");
    Serial.println(Z_RESULT);
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
      //MySerial0.print(X_RESULT);
      Serial.print(",");
      //MySerial0.print(",");
      Serial.print(Y_RESULT);
      //MySerial0.print(Y_RESULT);
      Serial.print(",");
      //MySerial0.print(",");
      Serial.print(Z_RESULT);
      //MySerial0.print(Z_RESULT);
      if (i != nDevices) {
        Serial.print(",");
        //MySerial0.print(",");
      }
    }
    Serial.println();
    //MySerial0.println();
  }
}



void reset_Addresses() {}


void assign_Addresses() {
  //I2C_ADDRESS Register (Offset = Ch) [Reset = 6Ah]
  //7-bit default factory I2C address is loaded from OTP during first
  //power up. Change these bits to a new setting if a new I2C address
  //is required (at each power cycle these bits must

  // Serial.println("Assigning Addresses");

  // Serial.println("Resetting Addresses");

  // digitalWrite(sensor1, HIGH);
  // digitalWrite(sensor2, HIGH);
  // digitalWrite(sensor3, HIGH);
  // delay(10);
  // IIC_Write(General_CALL_ADDRESS, REG_I2C_ADDRESS, I2C_ADDRESS_RESET);
  // delay(10);



  // digitalWrite(sensor1, HIGH);
  // digitalWrite(sensor2, LOW);
  // digitalWrite(sensor3, LOW);
  // delay(10);
  // IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_2_ADDRESS);
  // delay(10);

  // digitalWrite(sensor1, HIGH);
  // digitalWrite(sensor2, HIGH);
  // digitalWrite(sensor3, LOW);
  // delay(10);
  // IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_3_ADDRESS);
  // delay(10);

  // digitalWrite(sensor1, HIGH);
  // digitalWrite(sensor2, HIGH);
  // digitalWrite(sensor3, HIGH);
  // delay(10);
  // IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_4_ADDRESS);
  // delay(10);

  // Serial.println("Done Assigning Addresses");

  // Automate this process
  Serial.println("Assigning Addresses");
  // Set all sensors to high using array 
  for (int i = 0; i < 6; i++) {
    digitalWrite(sensorPins[i], HIGH);
  }
  delay(10);
  // Reset all sensors
  IIC_Write(General_CALL_ADDRESS, REG_I2C_ADDRESS, I2C_ADDRESS_RESET);

  // Assign addresses
  // Set sensor 1 to high and the rest to low
  digitalWrite(sensorPins[0], HIGH);
  for (int i = 1; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_2_ADDRESS);
  delay(10);

  // Set sensor 2 to high and the following to low
  digitalWrite(sensorPins[1], HIGH);
  for (int i = 2; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_3_ADDRESS);
  delay(10);

  // Set sensor 3 to high and the following to low
  digitalWrite(sensorPins[2], HIGH);
  for (int i = 3; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_4_ADDRESS);
  delay(10);

  // Set sensor 4 to high and the following to low
  digitalWrite(sensorPins[3], HIGH);
  for (int i = 4; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_5_ADDRESS);
  delay(10);

  // Set sensor 5 to high and the following to low
  digitalWrite(sensorPins[4], HIGH);
  for (int i = 5; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_6_ADDRESS);
  delay(10);

  // Set sensor 6 to high and the following to low
  digitalWrite(sensorPins[5], HIGH);
  delay(10);
  IIC_Write(DEVICE_1_ADDRESS, REG_I2C_ADDRESS, NEW_DEVICE_7_ADDRESS);
  delay(10);

  Serial.println("Done Assigning Addresses");

}





// ------------------ ESP-NOW Functions ------------------
void InitESPNow() {
  WiFi.disconnect();
  if (esp_now_init() == ESP_OK) {
    Serial.println("ESPNow Init Success");
  } else {
    Serial.println("ESPNow Init Failed");
    ESP.restart();
  }
}
// Scan for slaves in AP mode
void ScanForSlave() {
  int16_t scanResults = WiFi.scanNetworks(false, false, false, 300, CHANNEL); // Scan only on one channel
  // reset on each scan
  bool slaveFound = 0;
  memset(&slave, 0, sizeof(slave));

  Serial.println("");
  if (scanResults == 0) {
    Serial.println("No WiFi devices in AP Mode found");
  } else {
    Serial.print("Found "); Serial.print(scanResults); Serial.println(" devices ");
    for (int i = 0; i < scanResults; ++i) {
      // Print SSID and RSSI for each device found
      String SSID = WiFi.SSID(i);
      int32_t RSSI = WiFi.RSSI(i);
      String BSSIDstr = WiFi.BSSIDstr(i);

      if (PRINTSCANRESULTS) {
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.print(SSID);
        Serial.print(" (");
        Serial.print(RSSI);
        Serial.print(")");
        Serial.println("");
      }
      delay(10);
      // Check if the current device starts with `Slave`
      if (SSID.indexOf("Slave") == 0) {
        // SSID of interest
        Serial.println("Found a Slave.");
        Serial.print(i + 1); Serial.print(": "); Serial.print(SSID); Serial.print(" ["); Serial.print(BSSIDstr); Serial.print("]"); Serial.print(" ("); Serial.print(RSSI); Serial.print(")"); Serial.println("");
        // Get BSSID => Mac Address of the Slave
        int mac[6];
        if ( 6 == sscanf(BSSIDstr.c_str(), "%x:%x:%x:%x:%x:%x",  &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5] ) ) {
          for (int ii = 0; ii < 6; ++ii ) {
            slave.peer_addr[ii] = (uint8_t) mac[ii];
          }
        }

        slave.channel = CHANNEL; // pick a channel
        slave.encrypt = 0; // no encryption

        slaveFound = 1;
        // we are planning to have only one slave in this example;
        // Hence, break after we find one, to be a bit efficient
        break;
      }
    }
  }

  if (slaveFound) {
    Serial.println("Slave Found, processing..");
  } else {
    Serial.println("Slave Not Found, trying again.");
  }

  // clean up ram
  WiFi.scanDelete();
}

void deletePeer() {
  esp_err_t delStatus = esp_now_del_peer(slave.peer_addr);
  Serial.print("Slave Delete Status: ");
  if (delStatus == ESP_OK) {
    // Delete success
    Serial.println("Success");
  } else if (delStatus == ESP_ERR_ESPNOW_NOT_INIT) {
    // How did we get so far!!
    Serial.println("ESPNOW Not Init");
  } else if (delStatus == ESP_ERR_ESPNOW_ARG) {
    Serial.println("Invalid Argument");
  } else if (delStatus == ESP_ERR_ESPNOW_NOT_FOUND) {
    Serial.println("Peer not found.");
  } else {
    Serial.println("Not sure what happened");
  }
}

// Check if the slave is already paired with the master.
// If not, pair the slave with master
bool manageSlave() {
  if (slave.channel == CHANNEL) {
    if (DELETEBEFOREPAIR) {
      deletePeer();
    }

    Serial.print("Slave Status: ");
    // check if the peer exists
    bool exists = esp_now_is_peer_exist(slave.peer_addr);
    if ( exists) {
      // Slave already paired.
      Serial.println("Already Paired");
      return true;
    } else {
      // Slave not paired, attempt pair
      esp_err_t addStatus = esp_now_add_peer(&slave);
      if (addStatus == ESP_OK) {
        // Pair success
        Serial.println("Pair success");
        return true;
      } else if (addStatus == ESP_ERR_ESPNOW_NOT_INIT) {
        // How did we get so far!!
        Serial.println("ESPNOW Not Init");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_ARG) {
        Serial.println("Invalid Argument");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_FULL) {
        Serial.println("Peer list full");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_NO_MEM) {
        Serial.println("Out of memory");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_EXIST) {
        Serial.println("Peer Exists");
        return true;
      } else {
        Serial.println("Not sure what happened");
        return false;
      }
    }
  } else {
    // No slave found to process
    Serial.println("No Slave found to process");
    return false;
  }
}


// callback when data is sent from Master to Slave
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print("Last Packet Sent to: "); Serial.println(macStr);
  Serial.print("Last Packet Send Status: "); Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

// ------------------ Restart ESP32C3 function ------------------
void restartESP32C3() {
  Serial.println("Restarting ESP32C3...");
  ESP.restart();
}




// Copy readXYZ but include return of XYZ data
void readReturnXZY(int16_t *XYZ_RESULT){
  int16_t X_RESULT;
  int16_t Y_RESULT;
  int16_t Z_RESULT;

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
    X_RESULT = ((X_MSB << 8) | X_LSB);  // 16bits that make up the X channel data
    Y_RESULT = ((Y_MSB << 8) | Y_LSB);  // 16bits that make up the Y channel data
    Z_RESULT = ((Z_MSB << 8) | Z_LSB);  // 16bits that make up the Z channel data
    XYZ_RESULT[0] = X_RESULT;
    XYZ_RESULT[1] = Y_RESULT;
    XYZ_RESULT[2] = Z_RESULT;

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
      // Error check requestfrom data
      if (Wire.available()){
        byte X_MSB = Wire.read();
        byte X_LSB = Wire.read();
        byte Y_MSB = Wire.read();
        byte Y_LSB = Wire.read();
        byte Z_MSB = Wire.read();
        byte Z_LSB = Wire.read();
        byte DEV_CONF = Wire.read();
        X_RESULT = ((X_MSB << 8) | X_LSB);  // 16bits that make up the X channel data
        Y_RESULT = ((Y_MSB << 8) | Y_LSB);  // 16bits that make up the Y channel data
        Z_RESULT = ((Z_MSB << 8) | Z_LSB);  // 16bits that make up the Z channel data

        int index = i - 1;
        XYZ_RESULT[index * 3] = X_RESULT;
        XYZ_RESULT[index * 3 + 1] = Y_RESULT;
        XYZ_RESULT[index * 3 + 2] = Z_RESULT;
      } else {
        Serial.println("Error reading data");

        // Restart ESP32C3
        restartESP32C3();

        // // Redo assignment of addresses
        // // Delay for a moment 
        // delay(200);
        // assign_Addresses();
        // // Set reset flag
        // resetFlag = true;

      }
      

      // Serial.print(X_RESULT);
      // //MySerial0.print(X_RESULT);
      // Serial.print(",");
      // //MySerial0.print(",");
      // Serial.print(Y_RESULT);
      // //MySerial0.print(Y_RESULT);
      // Serial.print(",");
      // //MySerial0.print(",");
      // Serial.print(Z_RESULT);
      // //MySerial0.print(Z_RESULT);
      // if (i != nDevices) {
      //   Serial.print(",");
      //   //MySerial0.print(",");
      // }
    }
    // Serial.println();
    //MySerial0.println();
  }
  // Serial print array
  // for (int i = 0; i < nDevices * 3; i++) {
  //   Serial.print(XYZ_RESULT[i]);
  //   Serial.print(",");
  // }
  // Serial.println();
}

// // Function to send data to slave
// void sendData16Bit(const uint8_t *mac_addr, const int16_t *data, size_t dataSize) {
//   uint8_t sendBuffer[dataSize * 2];  // Each 16-bit value is represented by 2 bytes
//   for (size_t i = 0; i < dataSize; i++) {
//     sendBuffer[i * 2] = data[i] >> 8;  // High byte
//     sendBuffer[i * 2 + 1] = data[i] & 0xFF;  // Low byte
//   }
//   esp_err_t result = esp_now_send(mac_addr, sendBuffer, dataSize * 2);
//   if (result == ESP_OK) {
//     Serial.println("Sent with success");
//   } else {
//     Serial.println("Error sending the data");
//   }
// }



// ------------------ Setup ------------------

void setup() {

  // Delay for a bit 
  delay(1000);
  Serial.begin(115200);  // start serial for output
  //MySerial0.begin(115200, SERIAL_8N1, -1, -1);
  Serial.println("GPIO SET UP...");
  //MySerial0.println("GPIO SET UP...");


  Wire.begin();  // join i2c bus with address #4


  //pinMode(4, INPUT_PULLUP); //SDA internal pull up
  //pinMode(5, INPUT_PULLUP); //SCL internal pull up

  byte error, address;

  // pinMode(sensor1, OUTPUT);
  // pinMode(sensor2, OUTPUT);
  // pinMode(sensor3, OUTPUT);

  //set all sensors to output
  for (int i = 0; i < 6; i++) {
    pinMode(sensorPins[i], OUTPUT);
  }

  //set all sensors to low
  for (int i = 0; i < 6; i++) {
    digitalWrite(sensorPins[i], LOW);
  }

  // digitalWrite(sensor1, LOW);
  // digitalWrite(sensor2, LOW);
  // digitalWrite(sensor3, LOW);

  assign_Addresses();

  //Set all sensors to high
  for (int i = 0; i < 6; i++) {
    digitalWrite(sensorPins[i], HIGH);
  }

  // digitalWrite(sensor1, HIGH);
  // digitalWrite(sensor2, HIGH);
  // digitalWrite(sensor3, HIGH);



  Serial.println("Scanning...");
  //MySerial0.println("Scanning...");


  nDevices = 0;

  for (address = 1; address < 127; address++) {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      //Serial.print("I2C device found at address 0x");
      //MySerial0.print("I2C device found at address 0x");
      if (address < 16) {

        //Serial.print("0");
        //MySerial0.print("0");
      }
      //Serial.print(address, HEX);
      //MySerial0.print(address, HEX);
      //Serial.println("  !");
      //MySerial0.println("  !");

      nDevices++;
      deviceAddresses[nDevices] = address;

    } else if (error == 4) {
      //Serial.print("Unknown error at address 0x");
      //MySerial0.print("Unknown error at address 0x");
      if (address < 16) {
        //Serial.print("0");
        //MySerial0.print("0");
      }

      //Serial.println(address, HEX);
      //MySerial0.println(address, HEX);
    }
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
    Serial.println("CHECK WIRING AND RESTART");
    delay(1000);
    restartESP32C3();
    //MySerial0.println("No I2C devices found\n");
  } else {
    //Serial.println("done\n");
    //MySerial0.println("done\n");
  }



  configureDevice();
  setOperatingMode();


//   // ESPNOW SETUP
// //Set device in STA mode to begin with
//   WiFi.mode(WIFI_STA);
//   esp_wifi_set_channel(CHANNEL, WIFI_SECOND_CHAN_NONE);
//   Serial.println("ESPNow/Basic/Master Example");
//   // This is the mac address of the Master in Station Mode
//   Serial.print("STA MAC: "); Serial.println(WiFi.macAddress());
//   Serial.print("STA CHANNEL "); Serial.println(WiFi.channel());
//   // Init ESPNow with a fallback logic
//   InitESPNow();
//   // Once ESPNow is successfully Init, we will register for Send CB to
//   // get the status of Trasnmitted packet
//   esp_now_register_send_cb(OnDataSent);

// ESP Now setup
Serial.println("ESPNow Setting up..");
  WiFi.mode(WIFI_STA);
  InitESPNow();

  // Register peer
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = CHANNEL;
  peerInfo.encrypt = false;
  if (esp_now_add_peer(&peerInfo) == ESP_OK) {
    Serial.println("Peer added");
  } else {
    Serial.println("Failed to add peer");
  }


  // Update zero values
  int16_t ZerosSetupResult[nDevices * 3];
  readReturnXZY(ZerosSetupResult);
  for (int i = 0; i < nDevices * 3; i++) {
    ValuesArrayZero[i] = ZerosSetupResult[i];
  }

}




// ------------------ Health Check Functions ------------------
// Function that will read the sensors 5 tiimes and compare the values, if there are matching values between both reads then the sensors are broken 
void healthCheck(){
  // Read sensors twice
  int16_t ValuesArrayOne[nDevices * 3];
  int16_t ValuesArrayTwo[nDevices * 3];
  int16_t ValuesArrayThree[nDevices * 3];
  int16_t ValuesArrayFour[nDevices * 3];
  int16_t ValuesArrayFive[nDevices * 3];
  readReturnXZY(ValuesArrayOne);
  readReturnXZY(ValuesArrayTwo);
  readReturnXZY(ValuesArrayThree);
  readReturnXZY(ValuesArrayFour);
  readReturnXZY(ValuesArrayFive);

  // Compare the values
  // If there are two values that are matching in the same position then the sensors are broken 
  bool broken = false;
  for (int i = 0; i < 9; i++){
    if ((ValuesArrayOne[i] == ValuesArrayTwo[i]) && (ValuesArrayOne[i] == ValuesArrayThree[i]) && (ValuesArrayOne[i] == ValuesArrayFour[i]) && (ValuesArrayOne[i] == ValuesArrayFive[i])){
      broken = true;
    }
  }

  // If broken, restart ESP32C3  
  if (broken){
    Serial.println("Sensors are broken, restarting ESP32C3");
    restartESP32C3();
  }
}

int pos = 0;
void loop() {

  

  // Serial print number of devices
  // Serial.print("Number of devices: ");
  // Serial.println(nDevices);

  // Array to store XYZ data
  int16_t XYZ_RESULT[nDevices * 3];
  // Array to store filtered XYZ data
  int16_t XYZ_RESULT_FILTERED[nDevices * 3];

  // TEMPORARY CODE
  // If values array is all zeros, read XYZ data and store it to zero array 
  // grab global array ValuesArrayZero
  // if (ValuesArrayZero[0] == 0 && ValuesArrayZero[1] == 0 && ValuesArrayZero[2] == 0) {
  //   // Serial.println("ValuesArrayZero is all zeros");
  //   delay(500);
  //   readReturnXZY(ValuesArrayZero);
  // }

  // // If resetFlag is true, redo zero array 
  // if (resetFlag) {
  //   // Serial.println("Resetting ValuesArrayZero");
  //   delay(500);
  //   readReturnXZY(ValuesArrayZero);
  //   resetFlag = false;
  // }


  

  if (rawMode == 1) {

    // readXYZData();
    // Read XYZ data and store in array
    readReturnXZY(XYZ_RESULT);

    // Store the difference between the zero array and the XYZ array using abs but keep the sign
    // This will keep the direction in the axis while also zeroing the values
    for (int i = 0; i < nDevices * 3; i++) {
      XYZ_RESULT[i] = XYZ_RESULT[i] - ValuesArrayZero[i];
      // XYZ_RESULT_FILTERED[i] = XYZ_RESULT[i] - ValuesArrayZero[i];
    }


    // // Serial print array
    // for (int i = 0; i < nDevices * 3; i++) {
    //   Serial.print(XYZ_RESULT[i]);
    //   Serial.print(",");
    // }
    // Serial.println();

    // // Serial print array
    // for (int i = 0; i < nDevices * 3; i++) {
    //   Serial.print(XYZ_RESULT_FILTERED[i]);
    //   Serial.print(",");
    // }
    // Serial.println();

    // Print zeros array 
    // for (int i = 0; i < nDevices * 3; i++) {
    //   Serial.print(ValuesArrayZero[i]);
    //   Serial.print(",");
    // }
    // Serial.println();


    // Store data in packet
    DataPacket dataPacket;
    for (int i = 0; i < nDevices * 3; i++) {
      dataPacket.values[i] = XYZ_RESULT[i];
    }

    // Make a random data package with N devices
    // for (int i = 0; i < NUM_VALUES; i++) {
    // dataPacket.values[i] = random(-32768, 32767);  // Generate 16-bit random values
    // }
    // print number of devices
    Serial.print("Number of devices: ");
    Serial.println(nDevices);
    Serial.println();

    // Serial print packet
    Serial.print("Packet: ");
    for (int i = 0; i < nDevices * 3; i++) {
      Serial.print(dataPacket.values[i]);
      Serial.print(",");
    }
    Serial.println();
    // Send packet
    esp_now_send(receiverMAC, (uint8_t *)&dataPacket, sizeof(dataPacket));
    // Serial.println("Sent packet");


    delay(100);

    // // Send a new packet that starts with the number of devices and then the data
    // DataPacket dataPacket2;
    // dataPacket2.values[0] = nDevices;
    // for (int i = 1; i < nDevices * 3 + 1; i++) {
    //   dataPacket2.values[i] = XYZ_RESULT[i - 1];
    // }
    // // Serial print packet
    // Serial.print("Packet: ");
    // for (int i = 0; i < nDevices * 3 + 1; i++) {
    //   Serial.print(dataPacket2.values[i]);
    //   Serial.print(",");
    // }
    // Serial.println();


    // Health check
    // healthCheck();
  }

  }






