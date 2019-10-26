# GO-E-Charger-MQTT-to-InfluxDB

GO-E Charger is a mobile charging platform for electric vehicles.
The device generates a hotspot and can be configured with that (local home wifi, MQTT server eg Mosquitto). 
I use it to charge my Renault Zoe at home. At the moment i dont have a high current connection so i use 230V with the go-e charge set to 6 ampere. 
Its enough to load over night and to set the heater in the morning :-).

At least i prefered this device because of its adjustable loading power and the smart MQTT interface to integrate it into my home monitoring system (MQTT, InfluxDB and Grafana running on Raspberry Pi)

This attached Python script reads, parses and remap the MQTT json string from GO-E-Charger and sores the values in a influx database


Run script on start up:

nano /etc/rc.local

add:

sleep 10s

su pi -c 'python3 /[path to the script].py' &


so...have fun :-)



