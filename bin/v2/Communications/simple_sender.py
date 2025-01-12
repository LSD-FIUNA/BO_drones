import threading

import paho.mqtt.client as mqtt


class Sender(object):
    def __init__(self):
        self.client = mqtt.Client("sender")

        self._mqtt_thread = threading.Thread(target=self.mqtt_thread)
        self._mqtt_thread.start()

        self.step = False

        self.ids = ["type", "longitude", "latitude", "value", "altitude", "drone", "timestamp"]

    def mqtt_thread(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('127.0.0.1', 1883, 60)
        self.client.loop_forever()

    def on_connect(self, _client, _, __, rc):
        print("Connected to MQTT server")
        self.client.subscribe("step")

    def should_update(self):
        if self.step:
            self.step = False
            return True
        else:
            return False

    def on_message(self, _client, user_data, msg):
        message = bool(msg.payload)
        if msg.topic == "step":
            self.step = message

    def send_new_sensor_msg(self, raw_x_y_val, _id=0, sensor="t"):
        msg = sensor + "," + raw_x_y_val + ",1," + str(_id) + ", 3"
        payload = dict(zip(self.ids, msg.split(",")))
        for key in payload:
            try:
                payload[key] = float(payload[key])
            except Exception as e:
                pass
        # print(str(payload))
        while not self.client.is_connected():
            # threading.Timer
            continue
        self.client.publish("sensors", str(payload))
        # print("Message {} sent".format(payload))

    def send_new_drone_msg(self, raw_x_y, idx=-0):
        msg = "{},{},{}".format(idx, raw_x_y[0], raw_x_y[1])
        payload = dict(zip(["id", "x", "y"], msg.split(",")))
        for key in payload:
            try:
                payload[key] = float(payload[key])
            except Exception as e:
                pass
        # print(str(payload))

        while not self.client.is_connected():
            # threading.Timer
            continue
        self.client.publish("drones", str(payload))

    def send_new_goal_msg(self, raw_x_y, idx=-0):
        msg = "{},{},{}".format(idx, raw_x_y[0], raw_x_y[1])
        payload = dict(zip(["id", "x", "y"], msg.split(",")))
        for key in payload:
            try:
                payload[key] = float(payload[key])
            except Exception as e:
                pass
        # print(str(payload))
        while not self.client.is_connected():
            # threading.Timer
            continue
        self.client.publish("goals", str(payload))

    def send_new_acq_msg(self, acq_f):
        # print(acq_f)
        while not self.client.is_connected():
            # threading.Timer
            continue
        self.client.publish("params", acq_f)
