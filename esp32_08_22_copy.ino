#include<BLEDevice.h>
#include<BLEServer.h>
#include<BLEUtils.h>
#include <BLEScan.h>
#include <HTTPClient.h>
#include <ESP32_easy_wifi_data.h>
#include<WiFi.h>
#define serviceID BLEUUID((uint16_t)0x1300)

int count=0;
int volts=0;
bool ble_scan_active=false;
bool connected=false;

//////wifi settings
const char ssid[]  = "Danny the epic";
const char password[] = "666666666";
//////

unsigned long ChannelNumber1 = 1;
const char * myWriteAPIKey = "3PPYQEYKEMPHRW5";
WiFiClient client;   
 BLEScan* pBLEScan;
 int scanTime = 5; //In seconds

BLECharacteristic customCharacteristic(
  BLEUUID((uint16_t)0x1A00),
  BLECharacteristic::PROPERTY_READ
  );

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
    }
};

void setup() {
  Serial.begin(9600);
  BLEDevice::init("ESP32BLE");
  
  delay(1000);
  
  BLEServer *MyServer =BLEDevice::createServer();
  BLEService *customService=MyServer->createService(serviceID); 
  customService->addCharacteristic(&customCharacteristic);
 
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks()); 
  pBLEScan->setActiveScan(true); 
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99); 
  
  MyServer->getAdvertising()->addServiceUUID(serviceID);
  MyServer->getAdvertising()->start();

  WiFi.begin(ssid,password);

  ThingSpeak.begin(client);
  
  delay(1000);
}

void loop() {

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  
  HTTPClient http;  
  HTTPClient http_get;  
  http.begin("http://192.168.1.107:5000/BLE");
  http_get.begin("http://192.168.165.120:5000/");
  http.addHeader("Content-Type", "text/plain");    
  int httpResponseCode = http.POST("12345");   //Send the actual POST request
  int httpResponseCode_get = http_get.GET();

  if(httpResponseCode>0)
  {
    Serial.println(httpResponseCode); 
     delay(3000);
   }
   else
   {
    Serial.println("Error on sending POST");
   }

  if(httpResponseCode_get>0)
  {
    Serial.println(httpResponseCode_get); 
    Serial.println("get");
    String payload=http_get.getString();
    Serial.println(payload);
     delay(3000);
   }
   else
   {
    Serial.println("Error on Getting");
   }

  http.end();  //Free resources*/

 //Serial.println(count);

count++;

}
