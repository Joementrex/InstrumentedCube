#include <esp_now.h>
#include <WiFi.h>

#define CHANNEL 1
#define NUM_VALUES 15

struct DataPacket {
  int16_t values[NUM_VALUES * 3];
};

void InitESPNow() {
  WiFi.disconnect();
  if (esp_now_init() == ESP_OK) {
    Serial.println("ESPNow Init Success");
  } else {
    Serial.println("ESPNow Init Failed");
    ESP.restart();
  }
}

void OnDataRecv(const uint8_t *mac_addr, const uint8_t *data, int data_len) {
  DataPacket *packet = (DataPacket *)data;
  
//  Serial.println("Received data from sender:");
//  Serial.print("Sender MAC: ");
//  for (int i = 0; i < 6; i++) {
//    Serial.print(mac_addr[i], HEX);
//    if (i < 5) Serial.print(":");
//  }
//  Serial.println();

  for (int i = 0; i < NUM_VALUES * 3; i++) {
    Serial.print("Value "); Serial.print(i); Serial.print(": ");
    Serial.println(packet->values[i]);
  }
  Serial.println("");
}

void setup() {
  Serial.begin(115200);
  Serial.println("ESPNow Receiver Example");

  WiFi.mode(WIFI_AP);
  WiFi.softAP("ReceiverAP", "password", CHANNEL);

  Serial.print("Receiver MAC: ");
  Serial.println(WiFi.softAPmacAddress());

  InitESPNow();
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // DO NOT EVER RUN THIS ON ITS OWN! IT FILLS UP THE SERIAL AND CANNOT BE UPLOADED TO! 
  // Keep the receiver running
   // Print mac address of this device
//  Serial.print("This MAC: ");
//  Serial.println(WiFi.softAPmacAddress());
//  delay(1000);
}