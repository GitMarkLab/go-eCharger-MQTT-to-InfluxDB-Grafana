# GO-E-Charger-MQTT-to-InfluxDB
This Python script reads, parses and remap the MQTT json string from GO-E-Charger and sores the values in a influx database


Run script on start up:

nano /etc/rc.local

add:

sleep 10s

su pi -c 'python3 /[path to the script].py' &



