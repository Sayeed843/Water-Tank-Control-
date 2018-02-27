#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "-------";          // WIFI Name
const char* password =  "--------";    //WIFI Password
const char* mqttServer = "-------";    //cloudmqtt server
const int mqttPort = 00000;            //cloudmqtt server port
const char* mqttUser = "-------";      //cloudmqtt server username
const char* mqttPassword = "------";   //cloudmqtt server password
const String MAC = "/WTC-231";         // Create an manutal MAC address for identify the machine
String topic;
int upperSensor = A0;
int lowerSensor = 5;
int motorOutput = 2;
int thresholdValue = 800;
char topicValue[15];
char macValue[15];
bool motorAction = false;


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

bool waterPumpControl(int upperSensorValue, bool lowerSensorValue, bool motorCondition)
{
    if(upperSensorValue < thresholdValue and !lowerSensorValue)
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
    Serial.println("Motor OFF condition-1");
  }
  else if(upperSensorValue > thresholdValue and !lowerSensorValue and motorCondition) 
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition-2"); 
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue and !motorCondition)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition -3");
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue and motorCondition)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    Serial.println("Motor ON condition-4");    
  }
  else 
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
    Serial.println("Motor OFF Condition -5");  
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
    }else{
      Serial.print("Failed with State");
      Serial.print(client.state());
      delay(2000);
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


//********************* SETUP ***************************//
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  wifiConnection();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callBack);
  //WiFi.begin(ssid, password);
  pinMode(upperSensor,INPUT);
  pinMode(lowerSensor,INPUT);
  pinMode(motorOutput,OUTPUT);
  digitalWrite(motorOutput,HIGH);
  //Serial.begin(9600);

}
//********************* <SETUP> ***************************//


//******************** LOOP ****************************//
void loop() {
  // put your main code here, to run repeatedly:
  int upperValue = analogRead(upperSensor);
  bool lowerValue = digitalRead(lowerSensor);
  Serial.print("Upper Value: ");
  Serial.println(upperValue);
  Serial.print("Lower Value: ");
  Serial.println(lowerValue);
  motorAction = waterPumpControl(upperValue,lowerValue,motorAction);
  
  if(motorAction){
    topic = "True";
  }else{
    topic = "False";
  }
  topic.toCharArray(topicValue,15);
  MAC.toCharArray(macValue,15);
  
  //motorAction.toCharArray(topic, 15);
  if (!client.connected()){
    reconnect();
  }
  client.loop();
  client.publish(macValue, topicValue);
  //client.publish("/WTC", +topicValue);
  delay(20000);
}
//******************* <LOOP> *****************************//
