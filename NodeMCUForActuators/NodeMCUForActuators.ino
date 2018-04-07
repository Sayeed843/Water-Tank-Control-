#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "TIME PASS";          // WIFI Name
const char* password =  "uLo$s_y0urt!me";    //WIFI Password
const char* mqttServer = "m12.cloudmqtt.com";    //cloudmqtt server
const int mqttPort = 13348;            //cloudmqtt server port
const char* mqttUser = "wvxwjqte";      //cloudmqtt server username
const char* mqttPassword = "EbeW6HIvrbuS";   //cloudmqtt server password
const String MAC = "/WTC-231";         // Create an manutal MAC address for identify the machine
String topic;
int motorOutput = 2;
int thresholdValue = 800;
bool motorAction = false;
char message[100];

WiFiClient espClient;
PubSubClient client(espClient);

//*********************** MOTOR_VALUE *************************//
int motorValue(boolean mStatus)
{
  if(mStatus)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}
//********************* <MOTOR_VALUE> ***************************//

//********************** AGENT FUNCTION **************************//

bool waterPumpControl(int upperSensorValue, int lowerSensorValue, bool motorCondition, int thresholdValue)
{
    if(upperSensorValue < thresholdValue and lowerSensorValue < thresholdValue)
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
    Serial.println("Motor OFF condition-1");
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue < thresholdValue and motorCondition == true) 
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition-2"); 
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue > thresholdValue and motorCondition == false)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition -3");
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue > thresholdValue and motorCondition == true)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition-4");    
  }
  else 
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
    Serial.println("Motor OFF Condition -4");  
  }
  delay(5000);
  return motorCondition;
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
 
  Serial.println();
  Serial.println("-----------------------");
 
}
//*************************** <callBack> ******************************//


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  wifiConnection();
  client.setServer(mqttServer, mqttPort);
  //WiFi.begin(ssid, password);
//  pinMode(motorOutput,OUTPUT);
//  digitalWrite(motorOutput,HIGH);


}

//******************** LOOP ****************************//
void loop() {
//  motorAction = waterPumpControl(upperValue,lowerValue,motorAction);
  
//  if(motorAction){
//    topic = "True";
//  }else{
//    topic = "False";
//  }
  
  //motorAction.toCharArray(topic, 15);
  if (!client.connected()){
    reconnect();
    client.setCallback(callBack);
  }
  client.loop();
  //client.publish(macValue, topicValue);
  //client.publish("/WTC", +topicValue);
  delay(2000);
}
//******************* <LOOP> *****************************//
