/*
 * 第二组：基于RFID、蓝牙的智能门锁
 * 小组成员：王文博（队长） 郭宇、王昊
 * 结题时间： 2019/10/19  15:42
 */

/*
  引脚定义：
   RST          9             5         D9         RESET/ICSP-5     RST
   SDA(SS)      10            53        D10        10               10
   MOSI         11 / ICSP-4   51        D11        ICSP-4           16
   MISO         12 / ICSP-1   50        D12        ICSP-1           14
   SCK          13 / ICSP-3   52        D13        ICSP-3           15
   蓝牙：RX-Tx TX-Rx
   舵机：4 
   蜂鸣器： 8 
*/
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9
#define Clock_PIN 8
#define passUid  107

/*--------------------------------------------------------------------------常量定义*/
Servo myservo;  // 定义Servo对象来控制
int pos = 0; 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key; 

int length = 15; // 旋律的长度
char notes[] = "ccggaagffeeddc "; // 旋律音阶
int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 };
int tempo = 300;
byte nuidPICC[4];

/*--------------------------------------------------------------------------子函数定义*/
//将字节流按16进制输出
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
//将字节流按10进制输出
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}
//发出单音阶
void playTone(int tone, int duration) {
  for (long i = 0; i < duration * 1000L; i += tone * 2) {
    digitalWrite(Clock_PIN, HIGH);
    delayMicroseconds(tone);
    digitalWrite(Clock_PIN, LOW);
    delayMicroseconds(tone);
  }
}
//弹奏一段旋律
void playNote(char note, int duration) {
  char names[] = { 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'C' };
  int tones[] = { 1915, 1700, 1519, 1432, 1275, 1136, 1014, 956 };
 
  // play the tone corresponding to the note name
  for (int i = 0; i < 8; i++) {
    if (names[i] == note) {
      playTone(tones[i], duration);
    }
  }
}


/*-----------------------------------------------------------------------------初始化、循环运行*/
void setup() { 

  myservo.attach(4);  // 控制线连接数字4
  Serial.begin(9600); // 蓝牙、RFID统一波特率为9600
  pinMode(8,OUTPUT);
  
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 
  
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  //显示卡片信息，调试用
  Serial.println(F("This code scan the MIFARE Classsic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}
 
void loop() {

  //读取卡片id
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if ( ! rfid.PICC_ReadCardSerial())
    return;


  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);

  // 检查卡片类型，仅下列型号可用
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }
  //如果为记录好的passUID，响起小星星，启动舵机，蓝牙发送提示信息。
    if(*rfid.uid.uidByte==passUid){
        Serial.write("open the door with 107");
        for (int i = 0; i < length; i++) {
            if (notes[i] == ' ') {
                  delay(beats[i] * tempo); // rest
              }
             else{
                  playNote(notes[i], beats[i] * tempo);
              }
            // pause between notes
            delay(tempo / 2); 

            for (pos = 0; pos <= 360; pos ++) { 
                myservo.write(pos);              // 舵机角度写入
                delay(1);                       // 等待转动到指定角度
              }
          }
      Serial.println();
      }
  //否则，响起报警声，蓝牙发送安全警告
    else{
         Serial.write("unlegal try!");

         for (byte i = 0; i < 200; i++){
            digitalWrite(Clock_PIN, HIGH);
            delay(1);  
            digitalWrite(Clock_PIN, LOW);
            delay(1);  
         }
         Serial.println();
      }
    
  //结束RFID数据交换
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}
