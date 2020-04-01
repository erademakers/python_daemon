import requests
import ventilator_protocol as proto

class APIRequest():

    def __init__(self, base_address):
        self.base_address = base_address

    def __put(self, endpoint, data):
        try:
            r = requests.put(url = self.base_address + endpoint, data = data) 
            data = r.json()

            if not data["result"]:
                print("The request was not successful")
        except requests.RequestException:
            print("Couldn't reach the server")

    def send_setting_float(self, key, val):
        print("Send float setting to server, set to {}".format({key:float(val)}))
        self.__put("/api/settings?returncomplete=false", {key:float(val)})

    def send_setting(self, key, val):
        print("Send setting to server, set to {}".format({key:val}))
        self.__put("/api/settings?returncomplete=false", {key:val})

    def send_error(self, val):
        # self.__put("/api/settings", {'alarmValue':val})
        # print("todo; send the alarm")
        return
