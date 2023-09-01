import paho.mqtt.client as mqtt
import time

name =  input("Please enter your name ")
school = input("Please enter your school ")
topic = input("Please enter the topic you want to connect to ")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:
        print("Connection failed")

Connected = False  # global variable for the state of the connection
client = mqtt.Client()
client.on_connect = on_connect
client.connect("2.tcp.eu.ngrok.io", 17913, 60)
client.loop_start()  # start the loop
    

while Connected != True:  # Wait for connection
    time.sleep(0.1)
    
joined = name + " joined"
client.publish(topic, joined)

try:
    client.publish(topic, "Hello")
    while True:
        message = input('Your message: ')
        sender = school + " " + name + " : " +message
        client.publish(topic, sender)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()