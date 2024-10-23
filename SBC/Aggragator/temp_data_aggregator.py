import paho.mqtt.client as mqtt

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    msg = f"Topic: {message.topic}\nMessage: {message.payload.decode()}\n"
    print(msg)  # Print the message to the console
    with open("mqtt_messages.txt", "a") as file:
        file.write(msg + "\n")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Connect to the local MQTT broker (running on the same Raspberry Pi)
client.connect("localhost", 1883, 60)

# Subscribe to the desired topic
client.subscribe("your/topic")

# Start the MQTT client loop
client.loop_forever()
