import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import machine
from math import sqrt
from ads1115 import ADS1115
from consts import networkID,networkPassword, mqtt_server,client_id,topic_pub,powerFactor
from time import sleep_ms, ticks_ms, ticks_us


##########################
####Setting up WIFI#######
##########################
print("tring to connect to " + networkID)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(networkID,networkPassword)

print("connecting to \"" + networkID + " \" ")

#retry to connect to wifi if failed
time.sleep(1)
print(wlan.isconnected())
while(not wlan.isconnected()):
    print("not connected to wifi")
    time.sleep(10)
    wlan.connect(networkID,networkPassword)

        
##########################
#Connecting to MQTT#######
##########################
def mqtt_connect():    
    client = MQTTClient(client_id, mqtt_server,user="brenden", password="password", keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
print("connecting to \"" + mqtt_server + " \" ")
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    

##########################
########ADC Reads#########
##########################

ADC_RATE = 5 # delay rate in milliseconds

class ADC:
    def __init__(self, ADS,maxCurrent,maxVoltage, channel1, channel2 = None):
        self.ADS = ADS
        self.maxCurrent = maxCurrent
        self.maxVoltage = maxVoltage
        self.readTotal = 0
        self.readCount = 0
        self.channel1 = channel1
        self.channel2 = channel2
    def read(self):       
        self.ADS.set_conv(7,self.channel1, self.channel2)
        
        for x in range(0, 120):
            sleep_ms(ADC_RATE)
            self.readTotal += self.ADS.read_rev() ** 2.0
            self.readCount +=1
        
    def getAmps(self):
        voltage = self.ADS.raw_to_v(sqrt(self.readTotal/ self.readCount ))
        current = (self.maxCurrent / self.maxVoltage) * voltage 
        print("voltage " + str(voltage))
        print("current " + str(current))
        self.readTotal = 0
        self.readCount = 0
        return current  
    

class MQTT_adc:
    def __init__(self, mqttClient, ADC,topic):
        self.mqttClient = mqttClient
        self.ADC = ADC
        self.topic = topic
    def takeReading(self):
        self.ADC.read()
        amps = self.ADC.getAmps()
        watts = 120 * amps * powerFactor
        kWats = (watts/1000)
        if(kWats < 0.0005):
            kWats = 0
        kWatsString = bytearray(str(kWats).encode('utf-8'))
        self.mqttClient.publish(self.topic, kWatsString)

        print(kWatsString)
        


##########################
#Putting it all together##
##########################
i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14))

#TED clamps 4.096 200 amp 
TedADS = ADS1115(i2c,address=0x48, gain=1)
Ted1 = ADC(TedADS,200,3, 0)
Ted2 = ADC(TedADS,200,3, 1)

#YMDC clamps 4.096 100 amp 
YMDC_ADS = ADS1115(i2c,address=0x49, gain=1)
YMDC1 = ADC(YMDC_ADS,100,3,0,1)
YMDC2 = ADC(YMDC_ADS,100,3,2,3) 




listAdc = [
    #MQTT_adc(client,Ted1, topic_pub + "/leftMain"),
    MQTT_adc(client,Ted2, topic_pub + "/rightMain"),
    MQTT_adc(client,YMDC1, topic_pub + "/leftGarage"),
    #MQTT_adc(client,YMDC2, topic_pub + "/rightGarage")
] 

while(1):
    for adc in listAdc:
        adc.takeReading()


