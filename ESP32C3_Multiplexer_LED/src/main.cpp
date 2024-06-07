// This programs purpose is to interface with the ESP32C3 and the MCP23017 I/O expander
// The program will test communications with the MCP23017 and then set the pins to output

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MCP23X17.h>

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



// The multiplexer is connected to two 7 segment displays
// The first 7 segment display is connected to pins A7 to A4 and B0 to B3
// The second 7 segment display is connected to pins B4 to B7 and A3 to A0

// A7 to A4 goes left to right on the top set of pins
// B0 to B3 goes left to right on the bottom set of pins

// Store all pins in an array 
int pins[] = {PinA0, PinA1, PinA2, PinA3, PinA4, PinA5, PinA6, PinA7, PinB0, PinB1, PinB2, PinB3, PinB4, PinB5, PinB6, PinB7};

// Find the numbers 0 to 9 on the 7 segment display and map them to the pins
// int LeftZeroOn = [PinA7];


void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  // Initialize MCP23017 device
  mcp.begin_I2C(0x20);
  // Set all pins to output
  mcp.pinMode(0, OUTPUT);
  mcp.pinMode(1, OUTPUT);
  mcp.pinMode(2, OUTPUT);
  mcp.pinMode(3, OUTPUT);
  mcp.pinMode(4, OUTPUT);
  mcp.pinMode(5, OUTPUT);
  mcp.pinMode(6, OUTPUT);
  mcp.pinMode(7, OUTPUT);
  mcp.pinMode(8, OUTPUT);
  mcp.pinMode(9, OUTPUT);
  mcp.pinMode(10, OUTPUT);
  mcp.pinMode(11, OUTPUT);
  mcp.pinMode(12, OUTPUT);
  mcp.pinMode(13, OUTPUT);
  mcp.pinMode(14, OUTPUT);
  mcp.pinMode(15, OUTPUT);
  // Set all pins to low
  mcp.writeGPIOAB(0x0000);
}

void loop() {
  // // Set all pins to high
  // mcp.writeGPIOAB(0xFFFF);
  // // //Serial print on
  // //Serial.println("All pins set to high");
  // delay(1000);
  // // Set all pins to low
  // mcp.writeGPIOAB(0x0000);
  // // //Serial print off
  // //Serial.println("All pins set to low");
  // delay(1000);

  for (int i = PinB4; i <= PinB7; i++) {
    // Set pin to high
    mcp.digitalWrite(i, HIGH);
    // //Serial print on
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to high");
    delay(50);
    // Set pin to low
    mcp.digitalWrite(i, LOW);
    // //Serial print off
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to low");
    delay(50);
  }

  // Loop through pins A4 to A7 and set them to high and low individually 
  for (int i = PinA0; i <= PinA7; i++) {
    // Set pin to high
    mcp.digitalWrite(i, HIGH);
    // //Serial print on
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to high");
    delay(50);
    // Set pin to low
    mcp.digitalWrite(i, LOW);
    // //Serial print off
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to low");
    delay(50);
  }

  // Loop through pins B0 to B2 and set them to high and low individually
  for (int i = PinB0; i <= PinB3; i++) {
    // Set pin to high
    mcp.digitalWrite(i, HIGH);
    // //Serial print on
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to high");
    delay(50);
    // Set pin to low
    mcp.digitalWrite(i, LOW);
    // //Serial print off
    //Serial.print("Pin ");
    //Serial.print(i);
    //Serial.println(" set to low");
    delay(50);
  }


  // Delay for a moment 
  delay(100);
  // Turn on all pins
  mcp.writeGPIOAB(0xFFFF);
  // //Serial print on
  //Serial.println("All pins set to high");
  delay(1000);
  // Turn off all pins
  mcp.writeGPIOAB(0x0000);
  // //Serial print off
  //Serial.println("All pins set to low");
  delay(1000);


}