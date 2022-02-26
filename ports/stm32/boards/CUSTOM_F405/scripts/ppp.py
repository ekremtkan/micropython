import time
import machine
import network
from machine import Pin


# gsm = machine.UART(1,tx=22, rx=21, timeout=1000,  baudrate=9600)
gsm = machine.UART(4, baudrate=115200, timeout=1000, timeout_char=45, rxbuf=64)
time.sleep(1)

#GSMMODULE
modul_power=Pin('PB12',Pin.OUT) #Guc enable
if modul_power.value() == 0:
    modul_power.high()


reset_pin=Pin('PD11',Pin.OUT) #reset pin
def moduleReset():
    i=0
    while True:
        print('pin on')
        reset_pin.on()
        time.sleep(2)
        reset_pin.off()
        print('pin off')
        time.sleep(5)
        i+=1
        gsm.write("AT\r\n")
        time.sleep(1)
        ret=gsm.readline()
        if ret:
            ret+=gsm.readline()
        else:
            ret=gsm.readline()
            
        print(ret)
        if ret:
            if 'AT' in ret:
                break
        if i >2:
            print('MRESET_FAILED')
            break
    
moduleReset()
try:
    gsm.write("AT\r\n")
    print(gsm.readline())
    print(gsm.readline())
    time.sleep(1)

    gsm.write("AT+CPIN?\r\n")
    print(gsm.readline())
    print(gsm.readline())
    time.sleep(1)

    gsm.write("AT+CREG?\r\n")
    print(gsm.readline())
    print(gsm.readline())
    time.sleep(1)

    gsm.write("AT+CNMI=0,0,0,0,0\r\n")
    print(gsm.readline())
    print(gsm.readline())
    time.sleep(1)

    gsm.write('AT+CGDCONT=1,"IP","internet"\r\n')
    print(gsm.readline())
    print(gsm.readline())
    time.sleep(1)

    gsm.write('AT+CGDATA="PPP",1\r\n')
    time.sleep(1)
    print(gsm.readline())
    print(gsm.readline())

    time.sleep(5)
     
    ppp = network.PPP(gsm)
    ppp.active(True)
    time.sleep(15)

    print(ppp.ifconfig())
except Exception as e:
    print('GSM FAILED')
