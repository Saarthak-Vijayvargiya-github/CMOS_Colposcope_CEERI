#include <Stepper.h>
#include <Arduino.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>
#define AUTOFOCUS_COMMAND 10      // Value sent by python code by triggering sendAutoFCommand()

const int stepsPerRevolution_focus_servo = 20;
const int stepsPerRevolution_zoom_servo = 50;

const int total_zoom_servo_steps=2317;
const int total_focus_servo_steps=3009;

int zoomSteps = 0; int zoomState = 0;
int focusSteps = 0;
int x = 0;

Stepper focus_stepper(stepsPerRevolution_focus_servo, 13, 11, 9, 10);
Stepper zoom_stepper(stepsPerRevolution_zoom_servo, 5, 6, 8, 2);

char command=0;
int zoom_index=0, current_steps_zoom=0, current_steps_focus=0;
const int zoom_in=A2, zoom_out=A1, focus_plus=7, focus_minus=12;    // Initially zoom_out=4
void check(); void checkAfter();

void setup ()
{
  focus_stepper.setSpeed(400);
  zoom_stepper.setSpeed(300);
  pinMode(zoom_in, INPUT);
  pinMode(zoom_out, INPUT);
  pinMode(focus_plus, INPUT);
  pinMode(focus_minus, INPUT);
  pinMode(A0, INPUT);
  pinMode(3, INPUT);
  Serial.begin(9600);
  start_position();
  Serial.println("START");
  Serial.setTimeout(1);
}

void start_position()
{
  for (int i=0; i<=(int)(total_zoom_servo_steps/stepsPerRevolution_zoom_servo); i++)
  {
    zoom_stepper.step(stepsPerRevolution_zoom_servo);
  }
  Serial.println ("Zoom lens moved to starting position");
   for (int i=0; i<(int)(total_focus_servo_steps/stepsPerRevolution_focus_servo); i++)
  {
    focus_stepper.step(-stepsPerRevolution_focus_servo);
  }
   Serial.println ("Focus lens moved to starting position");
   for (int i=0; i<13; i++)
  {
    zoom_stepper.step(-stepsPerRevolution_zoom_servo);
//    Serial.println(i);
  }
}

void loop ()
{
 int zoom_in_state=digitalRead(zoom_in);
 int zoom_out_state=digitalRead(zoom_out);
 int focus_plus_state=digitalRead(focus_plus);
 int focus_minus_state=digitalRead(focus_minus);
  x = Serial.readString().toInt();
//  Serial.print(x);
  if(x == AUTOFOCUS_COMMAND){
    autoFocusCheck();
    delay(100);
 }
 if (zoom_in_state==LOW)
 {
  current_steps_zoom=5*stepsPerRevolution_zoom_servo;
   zoom_stepper.step(-current_steps_zoom);
   zoomSteps = zoomSteps-current_steps_zoom;
//   Serial.println("ZOOM_IN");
   zoomState = 1;
   current_steps_zoom=0; 
   delay(1000);
 }
  if (zoom_out_state==LOW)
 {
  current_steps_zoom=5*stepsPerRevolution_zoom_servo;
   zoom_stepper.step(current_steps_zoom);
   zoomSteps = zoomSteps+current_steps_zoom;
//   Serial.println("ZOOM_OUT");
   zoomState = -1;
   current_steps_zoom=0;
   delay(1000);
 }
  if (focus_minus_state==LOW)
 {
   focus_stepper.step(stepsPerRevolution_focus_servo);
   focusSteps = focusSteps-stepsPerRevolution_focus_servo;
   delay(100);
//   Serial.println("FOCUS_MINUS");
 }
   if (focus_plus_state==LOW)
 {
   focus_stepper.step(-stepsPerRevolution_focus_servo);
   focusSteps = focusSteps+stepsPerRevolution_focus_servo;
   delay(100);
//   Serial.println("FOCUS_PLUS");
 }
}

void check(){
  x = Serial.readString().toInt();
  Serial.print(x);
  if(x == AUTOFOCUS_COMMAND){
    check();
 }
}

void autoFocusCheck(){
  for (int i=0; i<(int)(total_focus_servo_steps/(2*stepsPerRevolution_focus_servo)); i++)
  {
    focus_stepper.step(-2*stepsPerRevolution_focus_servo);
  }
  focusSteps = 0;
  Serial.print(1);
  delay(100);
  for (int i=0; i<(int)(total_focus_servo_steps/(2*stepsPerRevolution_focus_servo)); i++)
  {
    focus_stepper.step(2*stepsPerRevolution_focus_servo);
    focusSteps = focusSteps-2*stepsPerRevolution_focus_servo;
  }
  Serial.print(2);
  delay(500);
  checkAfter();
  x = 0;
}

void checkAfter(){
  x = Serial.readString().toInt();
  focus_stepper.step(focusSteps - (x*(-2*stepsPerRevolution_focus_servo)));
}

/************
 * For autofocus the code keeps checking if AUTOFOCUS_COMMAND is sent.
 * autoFocusCheck() is triggered when user presses the AutoFocus key (in this case 'a'). This makes lens come to the 
outside and then sends a byte (in this case 1).
 * Then lens traverses inside and sends a byte (in this case 2).
 * checkAfter() recieves the value of the loop having maximum focus from python code and lens is focussed accordingly.
************/