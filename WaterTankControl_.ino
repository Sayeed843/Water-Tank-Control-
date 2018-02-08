
//**********************************************************//
/* 
 * Project name: "Water Tank Control"
 * Createed by "Sayeed Bin Mozahid"
 * Daffodil International University 
 * Department of Software Engineering
 * Updated Feb 8, 2018
 */
//*********************************************************//

#include <SoftwareSerial.h>    // Code to use SoftwareSerial
#define MacAddress "M34AC75D"  // create a unique Mac Address
SoftwareSerial esp8266 = SoftwareSerial(2,3); // Rx, Tx

String apiKey = "HPJ61IC0OV07OA4J";   // Thingspeak Channel API Key
String ssid = "TIME PASS";            // Wifi Name
String password = "uLo$s_y0urt!me";   // Wifi Password

int upperSensor = A0;
int lowerSensor = A1;
int motorOutput = 7;
bool motorAction = false;
int thresholdValue = 800;


//******************** RESPONSE TIME ****************************//
void responseTime(int waitTime)
{
  long t = millis();
  char c;
  while(t+waitTime> millis())
  {
    if (esp8266.available())
    {
      c = esp8266.read();
      Serial.print(c);
    }
  }
}
//********************** <RESPONSE_TIME> **************************//


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


//********************** THING SPEAK WRITE **************************//
boolean thingSpeakWrite(boolean motorStatus)
{
  String cmd ="AT+CIPSTART=\"TCP\",\"";  //TCP connection
         cmd +="184.106.153.149";        // api.thingspeak.com
         cmd +="\",80";

  esp8266.println(cmd);       
  Serial.println(cmd);
  if(esp8266.find("Error"))
  {
    Serial.println("AT+CIPSTART Error");
    return false; 
  }

  String getStr = "GET /update?api_key=";
         getStr +=apiKey;
         getStr +="&field1=";
         getStr +=String(motorValue(motorStatus));
         getStr +="&field2=";
         getStr +=String(MacAddress);
         getStr +="\r\n";

  cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  esp8266.println(cmd);
  Serial.println(cmd);
  delay(100);
  if(esp8266.find(">"))
  {
    esp8266.print(getStr);
    Serial.println(getStr);
  }
  else
  {
    esp8266.println("AT+CIPCLOSE");
    Serial.println("AT+CIPCLOSE");
    return false;
  }
  return true;
}
//********************* <THING_SPEAK_WRITE> ***************************//


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


//********************* SETUP ***************************//
void setup() {
  // put your setup code here, to run once:
  Serial.println("Okay");
  //debug = true;
  digitalWrite(motorOutput,HIGH);
  Serial.begin(9600);
  esp8266.begin(9600);
  esp8266.println("AT+CWMODE=1");   // set esp8266 wifi module as client
  responseTime(1000);
  esp8266.println("AT+CWJAP=\""+ssid+"\",\""+password+"\"");
  responseTime(5000);
  Serial.println("Setup Completed");
}
//********************* <SETUP> ***************************//


//******************** LOOP ****************************//
void loop() {
  // put your main code here, to run repeatedly:
  int upperValue = analogRead(upperSensor);
  int lowerValue = analogRead(lowerSensor);
  Serial.print("Upper Value: ");
  Serial.println(upperValue);
  Serial.print("Lower Value: ");
  Serial.println(lowerValue);
  motorAction = waterPumpControl(upperValue,lowerValue,motorAction,thresholdValue);
  thingSpeakWrite(motorAction);
  delay(20000);
}
//******************* <LOOP> *****************************//
