import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code:" + str(rc))
    client.subscribe("$SYS")
    client.subscribe("8/motorised/north/0/0/traffic_light/0")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("91.121.165.36", 1883, 60)

client.publish("8/motorised/north/0/0/traffic_light/0", "Test Message")

client.loop_forever()