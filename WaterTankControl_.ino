int upperSensor = A0;
int lowerSensor = A1;
int motorOutput = 7;
bool motorAction = false;
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
    motorAction = false;
    Serial.println("Motor OFF");
  }
  else if(upperValue > thresholdValue and lowerValue < thresholdValue and motorAction == true) 
  {
    digitalWrite(motorOutput,LOW);
    motorAction = true;
    Serial.println("Motor ON"); 
  }
  else if(upperValue > thresholdValue and lowerValue > thresholdValue and motorAction == false)
  {
    digitalWrite(motorOutput,LOW);
    motorAction = true;
    Serial.println("Motor ON");
  }
  else 
  {
    digitalWrite(motorOutput,HIGH);
    motorAction = false;
    Serial.println("Motor OFF");  
  }
  delay(5000);


  

}
