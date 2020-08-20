import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print('mqtt connected')
	else:
		print('bad connection, returned code : ', rc)

def om_disconnect(client, userdata, flags, rc=0):
	print(str(rc))

def on_publish(client, userdata, mid):
	print('in on_pub callback mid: ', mid)

client = mqtt.Client(userdata='gateway')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect('192.168.0.62', 8883)
client.loop_start()
client.publish('sensors', json.dumps({"serialNumber":"SN-001", "model":"T1000", "temperature":199.2}))
client.loop_stop()
client.disconnect()
