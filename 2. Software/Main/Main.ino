int left_motor_pin = 3;
int right_motor_pin = 10;
int volt_pin = A0;
int left_speed = 188; // set initial speed for left motor
int right_speed = 188; // set initial speed for right motor
int left_target_speed = 188;
int right_target_speed = 188;
unsigned long left_previous_time = 0;
unsigned long right_previous_time = 0;
unsigned long volt_previous_time = 0;
const int interval = 50; // time interval in milliseconds
const int volt_interval = 500; // time interval in milliseconds for voltage measurement

void setup() {
  pinMode(left_motor_pin, OUTPUT);
  pinMode(right_motor_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'L') {
      left_target_speed = Serial.parseInt();
    }
    else if (cmd == 'R') {
      right_target_speed = Serial.parseInt();
    }
  }
  
  unsigned long current_time = millis();
  
  if (current_time - left_previous_time >= interval) {
    if (left_speed < left_target_speed) {
      left_speed++;
      analogWrite(left_motor_pin, left_speed);
    } else if (left_speed > left_target_speed) {
      left_speed--;
      analogWrite(left_motor_pin, left_speed);
    }
    left_previous_time = current_time;
  }
  
  if (current_time - right_previous_time >= interval) {
    if (right_speed < right_target_speed) {
      right_speed++;
      analogWrite(right_motor_pin, right_speed);
    } else if (right_speed > right_target_speed) {
      right_speed--;
      analogWrite(right_motor_pin, right_speed);
    }
    right_previous_time = current_time;
  }

  if (current_time - volt_previous_time >= volt_interval) {
      int sensorValue = analogRead(volt_pin);
      float voltage = sensorValue / (42.2);
      Serial.println(voltage);
      volt_previous_time = current_time;
  }
}