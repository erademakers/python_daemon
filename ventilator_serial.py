"""
Ventilator Serial Handler
"""
import serial
import queue
import time
import ventilator_protocol as proto


class SerialHandler():

    def __init__(self, db_queue, request_queue, out_queue, alarm_queue, port='/dev/ventilator', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            self.attempt_reconnection()

        self.request_queue = request_queue
        self.db_queue = db_queue # Enqueue to
        self.out_queue = out_queue
        self.alarm_queue = alarm_queue

    def queue_put(self, type, val):
        """
        Send values to all necessary queues

        Args:
            type (str): type to be sent
            val (int): value to be sent
        """
        self.db_queue.put({'type': type, 'val': val})
        self.alarm_queue.put({'type': type, 'val': val})

    def attempt_reconnection(self):
            self.ser = None
            try:
                self.ser = serial.Serial(self.port, self.baudrate)
            except:
                pass

    def run(self, name):
        self.ser = serial.Serial(self.port, self.baudrate)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        print("Starting {}".format(name))
        while True:
            try:
                msg = self.out_queue.get(block=False)
            except queue.Empty:
                msg = None

            if msg != None:
                msg_out = msg['type'] + "=" + str(msg['val']) + "\n"
                try:
                    self.ser.write(bytes(msg_out, 'ascii'))
                except:
                    self.attempt_reconnection()

            line = ""
            try:
                line = self.ser.readline()
            except:
                self.attempt_reconnection()

            if line == "":
                print("Unable to read from Serial")
                continue


            try:
                line = line[:-2] # strip out '\r\n'
                checksum = int(line[-1]) # get raw checksum value
                line = line[:-1]
                calculated_checksum = proto.compute_LRC(line)

                if checksum != calculated_checksum:
                    print(line)
                    print("Checksum does not match, discard")
                    print("key: {},"
                          "val: {},"
                          "checksum: {}, "
                          "calculated_checksum: {}".format(key,
                                                           int(val),
                                                           checksum,
                                                           calculated_checksum))
                    continue
                else:
                    print("checksum OK")

                line = line.decode('utf-8')
                tokens = line.split('=')
                key = tokens[0]
                val = tokens[1]

                if line.startswith(proto.alarm + '='):
                    self.alarm_queue.put({'type': 'ALARM', 'val': val})


                # handle measurements
                for msgtype in proto.measurements:
                    if line.startswith((msgtype + '=')):
                        self.queue_put(msgtype, val)

                # handle settings
                for msgtype in proto.settings:
                    if line.startswith((msgtype + '=')):
                        if proto.settings_values[msgtype] != val:
                            self.request_queue.put({'type': 'setting',
                                                    'key': msgtype,
                                                    'value': val})

            except:
                print("Unable to decode message as UTF-8. Discarding")
