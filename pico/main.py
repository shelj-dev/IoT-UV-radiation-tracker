import network
import time
import urequests
from machine import Pin


WIFI_SSID = "iot kids"
WIFI_PASSWORD = "bright kidoos"

SERVER_IP_URL = "http://10.189.178.236:8000/"

wifi_status = False



def connect_wifi():
    global wifi_status

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wifi_status = True
        print("WiFi connected:", wlan.ifconfig()[0])
        return

    if not wlan.isconnected():

        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 5
        while timeout > 0 and not wlan.isconnected():
            print("Waiting for connection...")
            time.sleep(1)
            timeout -= 1

    wifi_status = wlan.isconnected()

    if wifi_status:
        print("WiFi connected:", wlan.ifconfig()[0])
    else:
        print("WiFi failed")

def sensor_data():
    value = sensor_pin.value()
    print("Sensor value:", value)
    return value


def send_data(data):

    payload = {
        "sensor": data
    }

    url = SERVER_IP_URL + "myapp/get-sensor/"

    r = None

    try:
        r = urequests.post(url, json=payload)
        print("Server response:", r.text)

    except Exception as e:
        print("Send error:", e)

    finally:
        if r is not None:
            r.close()

def main():
    while True:
        connect_wifi()

        sensor = sensor_data()

        if wifi_status:
            send_data(sensor)
        
        time.sleep(1.5)

main()
