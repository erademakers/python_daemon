"""
Ventilator Serial Handler
"""
import serial
import queue
import time
import ventilator_protocol


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
                msg_out = msg['type'] + "=" + str(msg['val']) + "\r\n"
                try:
                    self.ser.write(bytes(msg_out, 'ascii'))
                except:
                    self.attempt_reconnection()

            line = ""
            try:
                line = self.ser.readline()
            except:
                self.attempt_reconnection()

            try:
                line = self.ser.readline()
            except:
                print("Failure reading from serial port")
                line = None

            if line:
                try:
                    line = line.decode('utf-8')
                except UnicodeDecodeError:
                    print("Failure decoding serial message, continuing")
                    if self.errorcounter == 0:
                        self.errorcounter += 1
                        print("utf-8 decode errorcounter: {}".format(self.errorcounter))
                        continue
                    else:
                        print("Repeatedly unable to decode serial messages, aborting!")
                    # TODO: At the start it can happen that we get an incorrect message
                    # due to incomplete data. I do a hard abort here to ensure that this only
                    # happens once. We need to determine what a tolerable level of failure is here.

                tokens = line.split('=', 1)
                val = tokens[-1].rstrip('\r\n')

                if line.startswith(ventilator_protocol.alarm + '='):
                    self.alarm_queue.put({'type': 'ALARM', 'val': val})


                # handle measurements
                for type in ventilator_protocol.measurements:
                    if line.startswith((type + '=')):
                        self.queue_put(type, val)

                # handle settings
                for type in ventilator_protocol.settings:
                    if line.startswith((type + '=')):
                        # Verify that the checksum is correct.
                        pass
