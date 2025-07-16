import paho.mqtt.client as mqtt
import time
import os
import sys

LOG_PATH = os.path.join("data", "log_iot.txt")
os.makedirs("data", exist_ok=True)
broker = "172.23.105.142"  # Hoặc IP của broker khác nếu chạy ngoài Docker

def on_message(client, userdata, msg):
    log_line = f"{time.time()},{msg.topic},{msg.payload.decode()}\n"
    with open(LOG_PATH, "a") as f:
        f.write(log_line)
    print(f"Log: {log_line.strip()}")

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT broker with code", rc)
    client.subscribe("iot/#")

try:
    client = mqtt.Client(client_id="logger", protocol=mqtt.MQTTv31) # Must use MQTTv31 for compatibility
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883)

    print("Listening for MQTT messages... Press Ctrl+C to stop.")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nStopped by user.")
    client.disconnect()
    client.loop_stop()
except Exception as e:
    print("Lỗi khi chạy MQTT client:", e)
    sys.exit(1)
