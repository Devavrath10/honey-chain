/* Honey Chain ESP32 hive-node prototype.
   Replace sensor stubs and credentials before hardware deployment. */
#include <WiFi.h>
#include <PubSubClient.h>
WiFiClient net; PubSubClient mqtt(net);
const char* HIVE_ID="HIVE-101";
float readTemperature(){return 34.2;} float readHumidity(){return 61.0;} float readWeight(){return 42.8;}
void setup(){Serial.begin(115200); /* connect WiFi + configure MQTT in deployment */}
void loop(){
  char payload[180];
  snprintf(payload,sizeof(payload),"{\"hiveId\":\"%s\",\"temperature\":%.1f,\"humidity\":%.1f,\"weight\":%.1f}",HIVE_ID,readTemperature(),readHumidity(),readWeight());
  Serial.println(payload);
  if(mqtt.connected()) mqtt.publish("honeychain/hives/telemetry",payload);
  delay(60000);
}