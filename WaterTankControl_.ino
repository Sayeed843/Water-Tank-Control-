//#include <EEPROM.h>

int upperSensor = A0;
int lowerSensor = A1;
int motorOutput = 7;
bool motorAction = false;
int thresholdValue = 800;

//uint8_t EEPROMaddress = 130;

void setup() {
  // put your setup code here, to run once:
  pinMode(upperSensor,INPUT);
  pinMode(lowerSensor,INPUT);
  pinMode(motorOutput,OUTPUT);
  digitalWrite(motorOutput,HIGH);
  Serial.begin(9600);
}

void loop() {
  //motorAction = EEPROM.read(EEPROMaddress);
  //Serial.print("Motor Action= ");
  //Serial.print(motorAction);
  int upperValue = analogRead(upperSensor);
  int lowerValue = analogRead(lowerSensor);
  Serial.print("Upper Value: ");
  Serial.println(upperValue);
  Serial.print("Lower Value: ");
  Serial.println(lowerValue);
  motorAction = waterPumpControl(upperValue,lowerValue,motorAction,thresholdValue);

}



// Agent function
bool waterPumpControl(int upperSensorValue, int lowerSensorValue, bool motorCondition, int thresholdValue)
{
    if(upperSensorValue < thresholdValue and lowerSensorValue < thresholdValue)
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
   //EEPROM.write(EEPROMaddress,motorAction);
    Serial.println("Motor OFF condition-1");
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue < thresholdValue and motorCondition == true) 
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    //EEPROM.write(EEPROMaddress,motorAction);
    Serial.println("Motor ON condition-2"); 
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue > thresholdValue and motorCondition == false)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    //EEPROM.write(EEPROMaddress,motorAction);
    Serial.println("Motor ON condition -3");
  }
  else if(upperSensorValue > thresholdValue and lowerSensorValue > thresholdValue and motorCondition == true)
  {
    digitalWrite(motorOutput,LOW);
    motorCondition = true;
    //EEPROM.write(EEPROMaddress,motorAction);
    Serial.println("Motor ON condition-4");    
  }
  else 
  {
    digitalWrite(motorOutput,HIGH);
    motorCondition = false;
    //EEPROM.write(EEPROMaddress,motorAction);
    Serial.println("Motor OFF Condition -4");  
  }
  delay(5000);
  return motorCondition;
}

