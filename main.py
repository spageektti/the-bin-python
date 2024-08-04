from machine import Pin, ADC, SPI
from time import sleep
import max7219.py

CLK_PIN = 18
DATA_PIN = 19
CS_PIN = 17

VERT_PIN = 26
HORZ_PIN = 27
SEL_PIN = 26

spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(CLK_PIN), mosi=Pin(DATA_PIN))
cs = Pin(CS_PIN, Pin.OUT)

num_matrices = 1
matrix = max7219.Matrix8x8(spi, cs, num_matrices)
matrix.brightness(7)
matrix.fill(0)
matrix.show()

vert_adc = ADC(Pin(VERT_PIN))
horz_adc = ADC(Pin(HORZ_PIN))
sel_pin = Pin(SEL_PIN, Pin.IN, Pin.PULL_UP)

maxX = num_matrices * 8 - 1
maxY = 7

x = 0
y = 0

def display_snake():
    matrix.pixel(x, y, 1)
    matrix.show()

while True:
    horz = horz_adc.read_u16() >> 8
    vert = vert_adc.read_u16() >> 8
    
    if vert < 75:
        y = min(y + 1, maxY)
    if vert > 180:
        y = max(y - 1, 0)
    if horz > 180:
        x = min(x + 1, maxX)
    if horz < 75:
        x = max(x - 1, 0)
    
    if sel_pin.value() == 0:
        pass

    display_snake()
    
    sleep(0.1)
