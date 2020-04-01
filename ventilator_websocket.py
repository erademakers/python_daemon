#!/usr/bin/python3
import websocket
import json
import asyncio
import websockets
import ventilator_protocol as proto


class WebsocketHandler():

    def send_msg(self, msg):
        """
        Send the json formatted message with the correctly incremented ID
        """
        self.id += 1
        msg['id'] = self.id
        print(msg)
        self.ws.send(json.dumps(msg))

    def handle_settings(self, settings):
        for key in proto.settings:
            if key in settings:
                print("send setting {}".format(key))
                self.serial_queue.put({'type': key, 'val': settings[key]})

    def raise_alarm(self):
        self.alarm_queue.put({'type': proto.alarm, 'val': 1})

    def subscribe(self, path):
        """
        Subscribe to updates
        """
        sub_msg = {"type":"sub"}
        path = "/api/" + path
        sub_msg['path'] = path
        self.send_msg(sub_msg)
        reply = self.ws.recv()
        print(reply)

    def do_handshake(self):
        hello_msg = {'type': 'hello', 'version': '2'}
        self.send_msg(hello_msg)
        reply = self.ws.recv()
        print(reply)
        try:
            msg = json.loads(reply)
            self.interval = msg['heartbeat']['interval']
            self.ws.settimeout(self.interval/1000)
        except:
            print("Could not parse handshake response")

    def run(self, name):
        print("Starting {}".format(name))

        self.ws = websocket.WebSocket()
        self.ws.connect(self.url)

        self.do_handshake()
        self.subscribe('settings')

        while True:
            try:
                json_msg = self.ws.recv()
            except:
                print("Timeout or socket closed: reconnecting")
                self.raise_alarm()
                self.ws.close()
                self.attempt_reconnect()
                self.do_handshake()
                self.subscribe('settings')
                continue

            try:
                msg = json.loads(json_msg)
                if msg['type'] == "ping":
                    reply = {'type': 'ping'}
                    self.send_msg(reply)
                elif msg['type'] == "pub":
                    if msg['path'] == "/api/settings":
                        payload = msg['message']
                        self.handle_settings(payload)
            except Exception as e:
                print("Invalid message from websockets {}".format(json_msg))
                print(e)

    def attempt_reconnect(self):
        while True:
            try:
                self.ws.connect(self.url)
                if self.ws.connected == True:
                    return
            except:
                continue

    def __init__(self, serial_queue, alarm_queue, addr='localhost', port=3001):
        self.url = "ws://" + addr + ":" + str(port) + "/"
        self.id = 1
        self.serial_queue = serial_queue
        self.alarm_queue = alarm_queue


if __name__ == "__main__":
    ws = WebsocketHandler()
    ws.run('websocket handler')
