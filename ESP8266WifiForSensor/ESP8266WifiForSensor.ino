#include <WiFiEspUdp.h>
#include <WiFiEspClient.h>
#include <WiFiEspServer.h>
//#include <WiFiEsp.h>

///#include <Adafruit_Sensor.h>

#include <SoftwareSerial.h>
#include <PubSubClient.h>

SoftwareSerial soft = SoftwareSerial(2,3); // TX, Rx
WiFiEspClient espClient;
PubSubClient client(espClient);

const char* ssid = "vivo 1603";     //"Research_LAB";          // WIFI Name
const char* password = "123456789";     //"diulab505";    //WIFI Password
const char* mqttServer = "m12.cloudmqtt.com";    //cloudmqtt server
const int mqttPort = 13348;            //cloudmqtt server port
const char* mqttUser = "wvxwjqte";      //cloudmqtt server username
const char* mqttPassword = "EbeW6HIvrbuS";   //cloudmqtt server password
const String MAC = "/WTC-231";         // Create an manutal MAC address for identify the machine
String topic;
int upperSensor = A0;
int lowerSensor = A1;
char topicValue[60];
char macValue[15];
int status = WL_IDLE_STATUS;


//void responseTime(int waitTime)
//{
//  long t = millis();
//  char c;
//  while(t+waitTime>millis())
//  {
////    Serial.print("millis=");
////    Serial.println(millis());
//
//    if(esp8266.available())
//    {
//      c=esp8266.read();
//      Serial.print(c);
//    }
//  }
//}


//*************************** WiFI Connection *************************//
void wifiConnection(){  
  soft.begin(9600);
  // initialize ESP module
  WiFi.init(&soft);
  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  Serial.println("Connecting to AP ...");
  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, password);
    //delay(500);
  }
  Serial.println("Connected to AP");
}

//*************************** <Wifi Connection> ***********************//

//*************************** Reconnect *******************************//
void reconnect(){
  while(!client.connected()){
    Serial.println("Connecting to MQTT");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword)){
      Serial.println("Connected");
    }else{
      Serial.print("Failed with State");
      Serial.print(client.state());
      //delay(2000);
    }
  }
}
//*************************** <Reconnect> *****************************//

//*************************** callBack ********************************//
void callBack(char* topic, byte* payload, unsigned int length){
    Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
}
//*************************** <callBack> ******************************//
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  wifiConnection();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callBack);
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callBack);
  //WiFi.begin(ssid, password);
  pinMode(upperSensor,INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
    int upperValue = analogRead(upperSensor);
    int lowerValue = analogRead(lowerSensor);
  String payload = ""; 
  payload += upperValue;
  payload += "/"; 
  payload += lowerValue;
  payload.toCharArray(topicValue,60);
  MAC.toCharArray(macValue,15);
  if (!client.connected()){
    reconnect();
  }
  client.loop();
  client.publish(macValue, topicValue);
  delay(2000);
}
