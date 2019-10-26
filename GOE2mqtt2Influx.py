# https://go-e.co/wp-content/uploads/2019/07/api_de.pdf

import paho.mqtt.client as mqtt
import json
from IPython.display import clear_output
import time
import datetime
from influxdb import InfluxDBClient
import logging


INFLUXDB_SERVER = "193.178.168.12"
influx_username = 'pi'
influx_pw = 'pw'
influx_databasename = 'ifx_db_name'

cahrger_name = 'go-eCharger'
charger_id   = 'CHARGER-ID'

# Remaped Name
device_tag = 'Device_44/charger/'

# Remap
map=[['time','tme',0],
     ['total_energy','eto',0],
     ['charge_status','car',0],
     ['loaded_energy','dws',0],	 
     ['switch_off_value','dwo',0],
     ['load_ampere','amp',0],        
     ['volt_phase_1','nrg',0],  
     ['volt_phase_2','nrg',1], 
     ['volt_phase_3','nrg',2], 
     ['volt_phase_n','nrg',3],  
     
     ['ampere_phase_1','nrg',4], 
     ['ampere_phase_2','nrg',5], 
     ['ampere_phase_3','nrg',6],  
     
     ['power_phase_1','nrg',7], 
     ['power_phase_2','nrg',8], 
     ['power_phase_3','nrg',9],    
     ['power_phase_n','nrg',10], 
     ['power_all','nrg',1],      
     
     ['effic_phase_1','nrg',11], 
     ['effic_phase_2','nrg',12], 
     ['effic_phase_3','nrg',13],    
     ['effic_phase_n','nrg',14]      
    ]
print(map)

def on_message(client, userdata, message):
    for i in range(10):
        clear_output(wait=True)
    msg = str(message.payload.decode("utf-8"))
    #print("message received: ", msg)
    #print("message topic: ", message.topic)
    parse_massage(message.topic,msg)
    
def parse_massage(topic,rec_msg):
    if topic == cahrger_name + '/' + charger_id + '/' + 'status':
        y = json.loads(rec_msg)
        for i in range(len(map)):
            if map[i][1] == "nrg":
                #print(device_tag + map[i][0],y[map[i][1]][map[i][2]])
                #client.publish(device_tag + map[i][0],y[map[i][1]][map[i][2]] , 1, True)
                remaped_name = device_tag + map[i][0]
                remaped_value = y[map[i][1]][map[i][2]]
            else:
				#print(device_tag + map[i][0],y[map[i][1]])
                #client.publish(device_tag + map[i][0],y[map[i][1]], 1, True)
                remaped_name = device_tag + map[i][0]
                remaped_value = y[map[i][1]]
            client.publish(remaped_name,remaped_value, 1, True)	
            send2influx(remaped_name,remaped_value)

def send2influx(db_name,db_val):
    receiveTime=datetime.datetime.utcnow()
    json_body = [
                {
                    "measurement": db_name,
                    "time": receiveTime,
                    "fields": {
                    "Int_value":  int(db_val),
                    "Float_value": db_val # only possible to send float with note Float_
                    }
                }
    ]
    logging.info(json_body)
    #    print("----->>>>> Finished writing to InfluxDB start <<<<----------- ")
    dbclient.write_points(json_body)
    #    print("----->>>>> Finished writing to InfluxDB end <<<<----------- ")
	
def on_connect(client, userdata, flags, rc):
    client.subscribe(cahrger_name + '/' + charger_id + '/' + '#')
    print("loop")


logging.basicConfig(level=logging.INFO)
dbclient = InfluxDBClient(INFLUXDB_SERVER, 8086, influx_username, influx_pw, database=influx_databasename)
 
 
BROKER_ADDRESS = "localhost"
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(BROKER_ADDRESS)
 
print("Connected to MQTT Broker: " + BROKER_ADDRESS)
 
client.loop_forever()