#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "vivo 1603";          // WIFI Name
const char* password =  "123456789";    //WIFI Password
const char* mqttServer = "m13.cloudmqtt.com";    //cloudmqtt server
const int mqttPort = 16144;            //cloudmqtt server port
const char* mqttUser = "tuzdocic";      //cloudmqtt server username
const char* mqttPassword = "Eg9MQUEajoeR";   //cloudmqtt server password
const String MAC = "/WTC-231";         // Create an manutal MAC address for identify the machine
String topic;
int motorOutput = 2;
int thresholdValue = 800;
char message[100];
char* messageA = "";

WiFiClient espClient;
PubSubClient client(espClient);

//********************** AGENT FUNCTION **************************//

void waterPumpControl(char c)
{
  char trueValue;
  trueValue='1';
  Serial.print("Payload: ");
  Serial.println(c);
  Serial.print("trueValue ");
  Serial.println(trueValue);
  if(c == trueValue){
    digitalWrite(2,LOW);
    Serial.println("Motor ON");
  }
  else{
    digitalWrite(2,HIGH);
    Serial.println("Motor OFF");
  }
}
//******************** <AGENT_FUNCTION> ****************************//

//*************************** WiFI Connection *************************//
void wifiConnection(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to the WiFi Network");
}
//*************************** <Wifi Connection> ***********************//

//*************************** Reconnect *******************************//
void reconnect(){
  while(!client.connected()){
    Serial.println("Connecting to MQTT");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword)){
      Serial.println("Connected");
      client.subscribe("/WTC-231"); 
//       client.subscribe("/#"); 
    }else{
      Serial.print("Failed with State");
      Serial.print(client.state());
      delay(2000);
    }
  }
}
//*************************** <Reconnect> *****************************//

//*************************** callBack ********************************//
void callBack(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  waterPumpControl(payload[0]);
  Serial.println();
  Serial.println("-----------------------");
 
}
//*************************** <callBack> ******************************//


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  wifiConnection();
  pinMode(motorOutput,OUTPUT);
  client.setServer(mqttServer, mqttPort);
  digitalWrite(motorOutput,HIGH);


}

//******************** LOOP ****************************//
void loop() {
  if (!client.connected()){
    reconnect();
    client.setCallback(callBack);
  }
  client.loop();
  delay(1000);
}
//******************* <LOOP> *****************************//
