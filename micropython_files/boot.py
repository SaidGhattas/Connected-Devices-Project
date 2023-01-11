from  ble_uart_peripheral import *
import monster
import machine
from machine import Pin
import time
import uasyncio
from machine import Pin
from neopixel import NeoPixel
import network
import time
import ssd1306
from machine import Pin, SoftI2C
import ssd1306
import dht
import ntptime
import utime

pin = Pin(33, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
async def blink():
    for i in range(3):
        np[0] = (250, 1, 25) 
        np.write()  
        await uasyncio.sleep_ms(500)
        np[0] = (1, 1, 25) 
        np.write()  
        await uasyncio.sleep_ms(500)
    np[0] = (0, 0, 0) 
    np.write()
    
async def blink2():
    for i in range(2):
        np[0] = (250, 0, 0) 
        np.write()  
        await uasyncio.sleep_ms(500)
        np[0] = (0, 250, 0) 
        np.write()  
        await uasyncio.sleep_ms(500)
    np[0] = (0, 0, 0) 
    np.write()
def bluetooth_play():
    ble = bluetooth.BLE()
    uart = BLEUART(ble)

    def on_rx():
        rx=uart.read().decode().strip()
        print("rx: ",rx)
        if rx == "!B705":
            monster.back_mx()
        elif rx == "!B804":
            monster.forward_mx()
            
        elif rx == "!B507":
            monster.jump()
        elif rx == "!B10;":
            monster.shoot()
            
            

    uart.irq(handler=on_rx)
    nums = [4, 8, 15, 16, 23, 42]
    i = 0


    uart.close()

pin_left = machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin_right = machine.Pin(39, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin_jump = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin_shoot = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_DOWN)

def start():
    bluetooth_play()
    while True:
        if pin_left.value() == 1:
            monster.back_mx2()
        if pin_right.value() == 1:
            monster.forward_mx2() 
        if pin_jump.value() == 1:
            monster.jump2()   
        if pin_shoot.value() == 1:
            monster.shoot2()
        
#defining the display        
# using default address 0x3C
i2c = SoftI2C(sda=Pin(23), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

#home screem


wlan = network.WLAN(network.STA_IF)
wlan.active(False)
wlan.active(True)

if not wlan.isconnected():
    print('connecting to network...')
    display.text("connecting.....",0, 0)
    wlan.connect('hi', '12345678')
    while not wlan.isconnected():
        pass
    uasyncio.run(blink2())
    
print('network config:', wlan.ifconfig())
# Update the time
t = ntptime.time()

tm = utime.gmtime(t+3600)
machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
time.localtime()

d = dht.DHT22(machine.Pin(27))

btn = Pin(15, Pin.IN, Pin.PULL_UP) 





while True:
    # create the display and clears it every time
    display.fill(0)
    display.text(str(time.localtime()[0:4]), 0, 0)
    display.text(str(time.localtime()[4:]),0, 10)
    #print temperature and humidity
    d.measure()
    display.text("T: "+str(d.temperature()), 0, 22)
    display.text("H: "+str(d.humidity()), 60, 22)
    display.show()
    time.sleep(0.5) # wait 1 second
    if btn.value()==0:
        break
        
print("Game Started")
display.fill(0)
display.text("connect your",0, 0)
display.text("controllers to ",0, 10)
display.text("start",0, 20)


display.show()
uasyncio.run(blink())

start()
