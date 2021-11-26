/*
 * Initial Author: ryand1011 (https://github.com/ryand1011)
 *
 * Reads data written by a program such as "rfid_write_personal_data.ino"
 *
 * See: https://github.com/miguelbalboa/rfid/tree/master/examples/rfid_write_personal_data
 *
 * Uses MIFARE RFID card using RFID-RC522 reader
 * Uses MFRC522 - Library
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 *
 * More pin layouts for other boards can be found here: https://github.com/miguelbalboa/rfid#pin-layout
*/

#include <SPI.h>
#include <MFRC522.h>
bool a=false;
#define RST_PIN         5           // Configurable, see typical pin layout above
#define SS_PIN          53          // Configurable, see typical pin layout above
String conteudo= "";
int entrada=6;
int saida=7;
int contador=0;
//int tensao=12;
//int sinal=11;
int gnd=13;
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance

int anterior=0;
//logica do ultrasonico

#define pino_trigger 8
#define pino_echo 9

#define pino_trigger1 11
#define pino_echo1 12


int limite=15;
#include <Ultrasonic.h>
Ultrasonic ultrasonic(pino_trigger, pino_echo);
Ultrasonic ultrasonic1(pino_trigger1, pino_echo1);
void setup() {
 
  pinMode(entrada,OUTPUT);
  pinMode(saida,OUTPUT);
  pinMode(gnd,OUTPUT);
 // pinMode(sinal,INPUT);
  //digitalWrite(tensao,HIGH);
  digitalWrite(entrada,HIGH);
  digitalWrite(saida,HIGH);
  digitalWrite(gnd,LOW);
  Serial.begin(9600);                                           // Initialize serial communications with the PC
  SPI.begin();                                                  // Init SPI bus
  mfrc522.PCD_Init();                                              // Init MFRC522 card
  Serial.println(F("Read personal data on a MIFARE PICC:"));    //shows in serial that it is ready to read
}

//*****************************************************************************************//
void loop() {
  
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    //logica para funcionar somente quando se aproximar do ultrassonico
 float cmMsec,cmMsec1;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
 long microsec1 = ultrasonic1.timing();
  cmMsec1 = ultrasonic1.convert(microsec1, Ultrasonic::CM);

  
 if(cmMsec<=limite  || cmMsec1<=limite){
  
  digitalWrite(gnd,HIGH);
    digitalWrite(entrada,LOW);
    digitalWrite(saida,LOW);
    delay(3);
    digitalWrite(entrada,HIGH);
    digitalWrite(saida,HIGH);
 }
 else{
  digitalWrite(gnd,LOW);
  digitalWrite(entrada,LOW);
    digitalWrite(saida,LOW);
 }
 //fim da logica
     // if (digitalRead(sinal) == HIGH){ //SE A LEITURA DO PINO FOR IGUAL A LOW, FAZ
      //  Serial.println("bloqueado"); //ACENDE O LED
  //}   
      //logica para ler resposta serial com o computador
  //char b=Serial.read();
  
  
 // if(b=='b'){
   // Serial.println("recebeu");
   // a=true;
 
   // delay(500);
   
  //}
  //logica para desbloquear a passagem, inserir aqui  
    //if(a==true){
     // a=false;
      //conteudo="";
     // Serial.println("desbloqueado");
   // }
    
 // } fim da logica com o computador

   return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
  
    return;
  }
  //Mostra UID na serial
  //Serial.print("UID da tag :");
  
  byte letra;
  if(a==false){
    
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     //Serial.print(mfrc522.uid.uidByte[i], HEX);
     conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
     
  }
  conteudo.toUpperCase();
  Serial.println(conteudo.substring(1));
  if(conteudo.substring(1)=="ED 47 B9 A5"){
   Serial.println("entrou");
    
      
    
    //inserir aqui a logica para funcionar o rfid
     digitalWrite(entrada,LOW);
     digitalWrite(gnd,HIGH);
       digitalWrite(saida,LOW);
       delay(2000);
        digitalWrite(gnd,LOW);
      
      
  }
  }
  conteudo="";
  
  delay(500);
  
  
 
}
