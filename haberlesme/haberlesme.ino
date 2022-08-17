int datafromuser = 0;
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  if(Serial.available()>0)
  {
    datafromuser=Serial.read();
  }
  if (datafromuser=='1')
  {
    Serial.println("Led yandı.");
    digitalWrite(13, HIGH);
  }
  else if (datafromuser=='0')
  {
    Serial.println("Led söndü.");
    digitalWrite(13, LOW);
  }

}