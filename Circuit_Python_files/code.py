
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
import time
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

import board
import digitalio
# setting the pins for the controller inputs
left = digitalio.DigitalInOut(board.A1)
left.direction = digitalio.Direction.OUTPUT

right = digitalio.DigitalInOut(board.A0)
right.direction = digitalio.Direction.OUTPUT

jump = digitalio.DigitalInOut(board.A2)
jump.direction = digitalio.Direction.OUTPUT

fire = digitalio.DigitalInOut(board.A3)
fire.direction = digitalio.Direction.OUTPUT


while True:
    # advertizing and waiting for connection
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Now we're connected

    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    if packet.button == ButtonPacket.LEFT:
                        left.value = True
                        time.sleep(0.2)
                        left.value = False
                        print("LEFT button pressed!")
                    elif packet.button == ButtonPacket.RIGHT:
                        right.value = True
                        time.sleep(0.2)
                        right.value = False
                        print("RIGHT button pressed!")
                    elif packet.button == ButtonPacket.UP:
                        jump.value = True
                        time.sleep(0.1)
                        jump.value = False
                        print("UP button pressed!")
                    elif packet.button == ButtonPacket.BUTTON_1:
                        fire.value = True
                        time.sleep(0.1)
                        fire.value = False
                        print("One button pressed!")
