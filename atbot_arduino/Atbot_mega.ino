//mega code for recieve
const int trigger_F1=51;  //odd tigger.   even  echo  
const int echo_F1=50;
const int trigger_F2=49;
const int echo_F2=48;
const int trigger_F3=47;
const int echo_F3=46;
const int trigger_L1=53;
const int echo_L1=52;
const int trigger_L2=23;
const int echo_L2=22;
const int trigger_L3=31;
const int echo_L3=30;
const int trigger_R1=29;
const int echo_R1=28;
const int trigger_R2=27;
const int echo_R2=26;
const int trigger_R3=13;
const int echo_R3=12;
const int trigger_T=33;
const int echo_T=32;

const int Led10=4;
const int Led11=2;

const int F=A2;   //uno=9
const int L=A0;  //uno=11
const int R=A1;  //uno=10
const int B=A3; //uno =6
const int VL=A5;  //uno 3 
const int VR=A4;   //uno 5


 
const int ML0=6,ML1=9,MR0=10,MR1=11;
const int threshold_F1=30;
const int threshold_F2=30;
const int threshold_F3=30;
const int threshold_R1=20;
const int threshold_R2=25;
const int threshold_R3=25;
const int threshold_L1=20;
const int threshold_L2=25;
const int threshold_L3=25;
const int threshold_T=25;

long UF1,UF2,UF3,UL1,UL2,UL3,UR1,UR2,UR3,UT;

void setup() {
  Serial.begin(9600);
  pinMode(trigger_F1, OUTPUT); 
  pinMode(echo_F1, INPUT);
  pinMode(trigger_F2, OUTPUT); 
  pinMode(echo_F2, INPUT);
  pinMode(trigger_F3, OUTPUT); 
  pinMode(echo_F3, INPUT);
  pinMode(trigger_R1, OUTPUT); 
  pinMode(echo_R1, INPUT);
  pinMode(trigger_R2, OUTPUT); 
  pinMode(echo_R2, INPUT);
  pinMode(trigger_R3, OUTPUT); 
  pinMode(echo_R3, INPUT);
  pinMode(trigger_L1, OUTPUT); 
  pinMode(echo_L1, INPUT);
  pinMode(trigger_L2, OUTPUT); 
  pinMode(echo_L2, INPUT);
  pinMode(trigger_L3, OUTPUT); 
  pinMode(echo_L3, INPUT);
  pinMode(trigger_T, OUTPUT); 
  pinMode(echo_T, INPUT);

   pinMode(ML0,OUTPUT);
   pinMode(ML1,OUTPUT);
   pinMode(MR0,OUTPUT);
   pinMode(MR1,OUTPUT);

    pinMode(Led10,OUTPUT);
  pinMode(Led11,OUTPUT);
  digitalWrite(Led11,LOW);

  pinMode(F,INPUT);
  pinMode(B,INPUT);
  pinMode(L,INPUT);
  pinMode(R,INPUT);
  pinMode(VL,INPUT);
  pinMode(VR,INPUT);
  
}

void loop() {
  //read_operation();
 obstcle_avoid();
//velocity_read();
}
void velocity_read()
{
  int rL=analogRead(VL);
  int rR=analogRead(VR);
  Serial.println(rL);

  
}
void read_operation()
{
int rF=analogRead(F);
int rL=analogRead(L);
int rR=analogRead(R);
int rB=analogRead(B);
  Serial.print("F  :");
  Serial.println(rF);
  Serial.print("L  :");
  Serial.println(rL);
  Serial.print("R  :");
  Serial.println(rR);
  Serial.print("B  :");
  Serial.println(rB);
  Serial.println("");
  if(rF==1023)
  {
    forward(240,240);
   digitalWrite(Led10,HIGH);
  delay(100);
  }
  else if(rL==1023)
  {
    Hleft(240,240);
   digitalWrite(Led10,HIGH);
  delay(100);
  }
  else if(rR==1023)
  {
    Hright(240,240);
   digitalWrite(Led10,HIGH);
  delay(100);
  } 
  else if(rB==1023)
  {
    back(240,240);
   digitalWrite(Led10,HIGH);
  delay(100);
  }
  else
  { 
    pause();
    digitalWrite(Led10,LOW);
  delay(100);
  }
}
void led_blink()
{
  digitalWrite(Led10,HIGH);
  delay(500);
  digitalWrite(Led10,LOW);
  delay(100);
}
void bucket()
{
    pause();
    delay(500);
    do{
          Hleft(240,240);
          sensor_F();
          delay(100);
         }while(!(UF1>threshold_F1&&UF2>threshold_F2&&UF3>threshold_F3&&UT>threshold_T));
         pause();
        delay(500);
        while(true){
        sensor_R();
        if(UR1>threshold_R1&&UR2>threshold_R2&&UR3>threshold_R3)
        {
          right(100);
        }
        else
        {
          forward(200,255);
        }
        }
}
void obstcle_avoid()
{
  sensor_F();
  sensor_L();
  sensor_R();
  if(UF1>threshold_F1&&UF2>threshold_F2&&UF3>threshold_F3&&UT>threshold_T)
  {
      //forward(200,255);
      read_operation();
      //led_blink();
  }
  else if(UF1<threshold_F1&&UF2<threshold_F2&&UF3<threshold_F3&&UT>threshold_T)
  {
    bucket();
  }
  else if(UL1>threshold_L1&&UL2>threshold_L2&&UL3>threshold_L3)
  {
    pause();
    delay(500);
    do{
          Hleft(240,240);
          sensor_F();
          delay(100);
         }while(!(UF1>threshold_F1&&UF2>threshold_F2&&UF3>threshold_F3&&UT>threshold_T));
         pause();
        delay(500);
  }
  else if(UR1>threshold_R1&&UR2>threshold_R2&&UR3>threshold_R3)
  {
    pause();
    delay(500);
    do{
          Hright(240,240);
          sensor_F();
          delay(100);
         }while(!(UF1>threshold_F1&&UF2>threshold_F2&&UF3>threshold_F3&&UT>threshold_T));
         pause();
        delay(500);
  }
}

void sensor_F()
{
   long raw_middle;
     digitalWrite(trigger_F1, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_F1, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_F1, LOW);  
     raw_middle = pulseIn(echo_F1, HIGH);
     UF1 = (raw_middle/2)/29.1;
     Serial.print(" UF1 : ");
     Serial.println(UF1);
     
     digitalWrite(trigger_F2, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_F2, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_F2, LOW);  
     raw_middle = pulseIn(echo_F2, HIGH);
     UF2 = (raw_middle/2)/29.1;
     Serial.print(" UF2 : ");
     Serial.println(UF2);
     
     digitalWrite(trigger_F3, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_F3, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_F3, LOW);  
     raw_middle = pulseIn(echo_F3, HIGH);
     UF3 = (raw_middle/2)/29.1;
     Serial.print(" UF3 : ");
     Serial.println(UF3);
     
     digitalWrite(trigger_T, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_T, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_T, LOW);  
     raw_middle = pulseIn(echo_T, HIGH);
     UT = (raw_middle/2)/29.1;
     Serial.print(" UT : ");
     Serial.println(UT);
}

    void sensor_R()
{
   long raw_middle;
     digitalWrite(trigger_R1, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_R1, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_R1, LOW);  
     raw_middle = pulseIn(echo_R1, HIGH);
     UR1 = (raw_middle/2)/29.1;
     Serial.print(" UR1 : ");
     Serial.println(UR1);
     
     digitalWrite(trigger_R2, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_R2, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_R2, LOW);  
     raw_middle = pulseIn(echo_R2, HIGH);
     UR2 = (raw_middle/2)/29.1;
     Serial.print(" UR2 : ");
     Serial.println(UR2);

     digitalWrite(trigger_R3, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_R3, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_R3, LOW);  
     raw_middle = pulseIn(echo_R3, HIGH);
     UR3 = (raw_middle/2)/29.1;
     Serial.print(" UR3 : ");
     Serial.println(UR3);
}
    void sensor_L()
{
   long raw_middle;
     digitalWrite(trigger_L1, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_L1, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_L1, LOW);  
     raw_middle = pulseIn(echo_L1, HIGH);
     UL1 = (raw_middle/2)/29.1;
     Serial.print(" UL1 : ");
     Serial.println(UL1);
     
     digitalWrite(trigger_L2, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_L2, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_L2, LOW);  
     raw_middle = pulseIn(echo_L2, HIGH);
     UL2 = (raw_middle/2)/29.1;
     Serial.print(" UL2 : ");
     Serial.println(UL2);
     
     digitalWrite(trigger_L3, LOW);  
     delayMicroseconds(2);               
     digitalWrite(trigger_L3, HIGH);   
     delayMicroseconds(10);               
     digitalWrite(trigger_L3, LOW);  
     raw_middle = pulseIn(echo_L3, HIGH);
     UL3 = (raw_middle/2)/29.1;
     Serial.print(" UL3 : ");
     Serial.println(UL3);
}
void forward(int L,int R)
{
  analogWrite(MR0,R);
  analogWrite(MR1,LOW);
  analogWrite(ML0,L);
  analogWrite(ML1,LOW);
}
void left(int R)
{
  analogWrite(MR0,R);
  analogWrite(MR1,LOW);
  analogWrite(ML0,LOW);
  analogWrite(ML1,LOW);
}
void right(int L)
{
  analogWrite(MR0,LOW);
  analogWrite(MR1,LOW);
  analogWrite(ML0,L);
  analogWrite(ML1,LOW);
}
void Hleft(int L,int R)
{
  analogWrite(MR0,R);
  analogWrite(MR1,LOW);
  analogWrite(ML0,LOW);
  analogWrite(ML1,L);
}
void Hright(int L,int R)
{
  analogWrite(MR0,LOW);
  analogWrite(MR1,R);
  analogWrite(ML0,L);
  analogWrite(ML1,LOW);
}
void pause()
{
  digitalWrite(MR0,LOW);
  digitalWrite(MR1,LOW);
  digitalWrite(ML0,LOW);
  digitalWrite(ML1,LOW);
}
void back(int L,int R)
{
  analogWrite(MR0,LOW);
  analogWrite(MR1,R);
  analogWrite(ML0,LOW);
  analogWrite(ML1,L);
}
