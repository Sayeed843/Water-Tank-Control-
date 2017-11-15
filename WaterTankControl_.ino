int upperSensor = A0;
int lowerSensor = A1;
int motorOutput = 7;
int thresholdValue = 800;
void setup() {
  // put your setup code here, to run once:
  pinMode(upperSensor,INPUT);
  pinMode(lowerSensor,INPUT);
  pinMode(motorOutput,OUTPUT);
  digitalWrite(motorOutput,HIGH);
  Serial.begin(9600);
}

void loop() {
  int upperValue = analogRead(upperSensor);
  int lowerValue = analogRead(lowerSensor);
  Serial.print("Upper Value: ");
  Serial.println(upperValue);
  Serial.print("Lower Value: ");
  Serial.println(lowerValue);
  if(upperValue < thresholdValue and lowerValue < thresholdValue)
  {
    digitalWrite(motorOutput,HIGH);
    Serial.println("Motor OFF");
  }
  else if(upperValue > thresholdValue and lowerValue > thresholdValue)
  {
    digitalWrite(motorOutput,LOW);
    Serial.println("Motor ON");
  }
  else 
  {
    digitalWrite(motorOutput,HIGH);
    Serial.println("Motor OFF");  
  }
  delay(5000);
//  
//  if(upperValue < thresholdValue and lowerValue < thresholdValue)
//  {
//    Serial.println("Upper and Lower Value don't want water!!!");
//  }
//  else if(upperValue > thresholdValue and lowerValue < thresholdValue)
//  {
//    Serial.println("Upper want to water");
//  }
//  else if(upperValue < thresholdValue and lowerValue > thresholdValue)
//  {
//    Serial.println("Lower want to water");
//  }
//  else
//  {
//    Serial.println("Both are want to water!!!");
//  }

  

}
