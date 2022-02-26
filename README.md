# STM32 MicroPython Examples

`These simple libraries have been tested on the STM32`

datetime.py

`Python datetime library is optimized for MicroPython`

![image](https://user-images.githubusercontent.com/72562273/150955960-108c1d7f-113d-46f8-bd61-8d8663ab73bc.png)


# ports/stm32/boards/CUSTOM_F405/scripts/dtime.py

`It is a simple library that can make date format changes. strftime and strptime examples`

![image](https://user-images.githubusercontent.com/72562273/150955097-5965083e-0ce7-4332-a23d-4da6d0f16290.png)

# /ports/stm32/boards/CUSTOM_F405/scripts/serial.py

`It is a simple library where you can adjust uart settings, read and write over uart.
It is an application that sends the read data to the ring buffer and pulls it from there if needed.`

```import serial 
#  (uart1,baudrate,bits (7-8-9) )
ser=serial.SerialPort(1,115200,7,DEBUG=12)
ser.open()
ser.write('test\r\n')
result=ser.read()
ser.write_Serial('%ctest5\r\n'%chr(15))
ser.set_globaltimeout(60)
ser.baudrate(9600)
result2=ser.read()
ser.baudrate(300)
.....
```

# /ports/stm32/boards/CUSTOM_F405/scripts/ppp.py
`Sim800c AT command examples`
