# main.py -- put your code here!
import time
import pyb,re
from machine import UART
from machine import Pin
def ledsOn():
    for led in 'PE7','PB1','PB0','PC5','PC4','PE11','PE12','PE8','PE9','PE10':
        try:
            l=eval('pyb.Pin(pyb.Pin.board.%s,mode=pyb.Pin.OUT)'%led)
            l.on()
            time.sleep(0.1)
        except:
            pass
def ledsOff():
    for led in 'PE7','PB1','PB0','PC5','PC4','PE11','PE12','PE8','PE9','PE10':
        try:
            l=eval('pyb.Pin(pyb.Pin.board.%s,mode=pyb.Pin.OUT)'%led)
            l.off()
            time.sleep(0.1)
        except:
            pass


def serial_write(ser,msg):
    rts.on()
    ser.write(msg)
    rts.off()

DEBUG=1


ledsOff()
ledsOn()

uart1 = UART(1, 115200)
uart1.init(115200, bits=8, parity=None, stop=1)
uart2 = UART(2, baudrate=300, bits=7, parity=0, stop=1, flow=0, timeout=100, timeout_char=45, rxbuf=64)
#uart2.init(115200, bits=8, parity=None, stop=1)
uart1.write('PYB:%s\r\n'%'---start---')
rts = pyb.Pin('PA0',mode=pyb.Pin.OUT)
uart1.write('PYB:%s\r\n'%dir(machine.Pin))
uart1.write('PYB:%s\r\n'%help('modules'))
