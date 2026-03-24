from machine import ADC, Pin
import time
import network
import urequests

# UV Sensor
uv = ADC(Pin(26))

# WiFi Credentials
WIFI_SSID = "iot kids"
WIFI_PASSWORD = "bright kidoos"

# Server URL
SERVER_IP_URL = "http://10.189.178.134:8000/api/uv-data/"


# Connect WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while timeout > 0:
            if wlan.isconnected():
                break
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig()[0])
        return True
    else:
        print("WiFi failed")
        return False


# Read UV
def read_uv():
    raw = uv.read_u16()
    voltage = raw * (3.3 / 65535)
    uv_index = voltage * 1000
    return raw, uv_index


# Send data
def send_data(uv_value):
    payload = {
        "uv_index": uv_value
    }

    try:
        response = urequests.post(SERVER_IP_URL, json=payload)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Send Error:", e)


# Main loop
def main():

    while True:

        # Ensure WiFi is connected
        if not connect_wifi():
            print("Retrying WiFi in 5 sec...")
            time.sleep(5)
            continue

        raw, uv_index = read_uv()

        print("Raw:", raw)
        print("UV Index:", uv_index)

        send_data(uv_index)

        # 🔥 Better delay (avoid spamming server)
        time.sleep(5)


# Run
main()