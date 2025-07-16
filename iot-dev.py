import paho.mqtt.client as mqtt
import time
import random
import json
import sys

# Kết nối đến MQTT Broker
broker = "172.23.105.142"  # Hoặc IP của broker khác nếu chạy ngoài Docker

try:
    client = mqtt.Client(client_id="iot_simulator", protocol=mqtt.MQTTv31) # Must use MQTTv31 for compatibility
    client.connect(broker, 1883, 60)
except Exception as e:
    print("Không thể kết nối đến MQTT broker:", e)
    sys.exit(1)

# Giả lập từng loại cảm biến
def simulate_temperature():
    temp = round(random.uniform(25.0, 40.0), 2)
    return {"device_id": "temp_sensor_1", "temperature": temp, "unit": "C", "version": "1.0"}

def simulate_door_sensor():
    status = random.choice(["open", "closed"])
    return {"device_id": "door_sensor_1", "status": status, "version": "1.0"}

def simulate_motion_camera():
    motion = random.choice([True, False])
    return {"device_id": "camera_1", "motion_detected": motion, "version": "1.0"}

# Vòng lặp gửi dữ liệu
try:
    while True:
        temp_data = simulate_temperature()
        door_data = simulate_door_sensor()
        camera_data = simulate_motion_camera()

        client.publish("iot/sensor/temperature", json.dumps(temp_data))
        client.publish("iot/sensor/door", json.dumps(door_data))
        client.publish("iot/sensor/camera", json.dumps(camera_data))

        print(f"Sent: {temp_data}, {door_data}, {camera_data}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nDừng giả lập.")
    client.disconnect()
