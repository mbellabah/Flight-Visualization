import processing.serial.*;

float pitch, roll;
float position;

Serial myPort;

void setup(){
   size(800, 800, P3D);
   smooth(32);

   position = width/2;
   
   println(Serial.list());
   
   myPort = new Serial(this, Serial.list()[1], 115200);
   myPort.bufferUntil('\n');
   
  
} 

void draw(){
   background(#20542E);
   fill(#79BF3D);
   tilt();
} 

void tilt(){
   translate(position, position, position);
   rotateX(radians(roll + 90));
   rotateY(radians(pitch));
   
   fill(#79BF3D);
   ellipse(0, 0, width/4, width/4);
   fill(#20542E);
   text(pitch + "," + roll, -40, 10, 1);
}

void serialEvent(Serial myPort){
   String myString = myPort.readStringUntil('\n');
   
   
   if (myString != null){
     myString = trim(myString);
     String items[] = split(myString, ',');
     if (items.length > 1){
       pitch = float(items[0]);
       roll = float(items[1]);
     }
   }
}