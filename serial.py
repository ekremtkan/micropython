from os import mkdir as os_mkdir,remove as os_remove,sync as os_sync
from time import time,sleep
from machine import UART
from pyb import Pin
from logging import getLogger

# logging.basicConfig(level=logging._INFO)
logger = getLogger("serial")
logger.level=1
# logger.debug("Test message: %d(%s)", 100, "foobar")
# logger.info("Test message2: %d(%s)", 100, "foobar")
# logger.warning("Test message3: %d(%s)")
# logger.error("Test message4")
# logger.critical("Test message5")
# logger.info("Test message6")

def mkdir(path):
    last_path=''
    state=True
    if path.startswith('/'):
        last_path='/'
    for p in path.split('/'):
        if not p:continue
        if last_path and last_path == '/':
            c_path='%s%s'%(last_path,p)
        elif last_path and last_path != '/':
            c_path='%s/%s'%(last_path,p)
        else:
            c_path=p
        try:
            if not c_path.endswith('flash'):
                os_mkdir(c_path)
        except Exception as e:
            if 'Errno 17' not in str(e):
                print('cant create dirctory (%s) err:%s'%(c_path,e))
                state=False
        last_path='%s'%c_path
    if state:
        os_sync()
    return state

class RINGBUFFER:
    def __init__(self, size):
        self.data = bytearray(size)
        self.size = size
        self.index_put = 0
        self.index_get = 0
        self.runing_write_file=True

    def put(self, value):
        next_index = (self.index_put + 1) % self.size
        # check for overflow
        if self.index_get != next_index:
            self.data[self.index_put] = value
            self.index_put = next_index
            return value
        else:
            return None
    def get(self):
        if self.index_get == self.index_put:
            return None  ## buffer empty
        else:
            value = self.data[self.index_get]
            self.index_get = (self.index_get + 1) % self.size
            return value
    def getAll(self):
        if self.index_get == self.index_put:
            return None
        else:
            ret=''
            while self.index_get != self.index_put:
                ret='%s%c'%(ret,chr(self.get()))
            return ret
    def getall(self):
        return self.data[self.index_get:self.index_put]

    def getAndPutValue(self,index=-1):
        if self.index_get == self.index_put:
            return None  ## buffer empty
        else:
            value = self.data[(self.index_put + index) % self.size]
            return value
    def filewrite(self,raw_file='raw_read.txt',mod='a'):
        f=open(raw_file,mod)
        while self.runing_write_file and  self.index_get != self.index_put:
            while self.index_get != self.index_put:
                f.write(chr(self.get()))
            sleep(1)
        f.close()

class ASCII:
    charToVal={ 'NUL': 0 , 'SOH': 1 , 'STX': 2 , 'ETX': 3 , 'EOT': 4 , 'ENQ': 5 ,'ACK': 6 , 'BEL': 7 , 'BS': 8 , 'HT': 9 , 'LF': 10, 'VT': 11,'FF': 12, 'CR': 13, 'SO': 14, 'SI': 15, 'DLE': 16, 'DCL': 17, 'DC2': 18, 'DC3': 19, 'DC4': 20, 'NAK': 21, 'SYN': 22, 'ETB': 23, 'CAN': 24, 'EM': 25, 'SUB': 26, 'ESC': 27, 'FS': 28, 'GS': 29, 'RS': 30, 'US': 31 ,'SP':32}
    valToChar={ 0:'NUL',1:'SOH',2:'STX',3:'ETX',4:'EOT',5:'ENQ',6:'ACK',7:'BEL',8:'BS',9:'HT',10:'LF' ,11:'VT' ,12:'FF',13:'CR' ,14:'SO' ,15:'SI',16:'DLE' ,17:'DCL' ,18:'DC2' ,19:'DC3' ,20:'DC4' ,21:'NAK' ,22:'SYN' ,23:'ETB' ,24:'CAN' ,25:'EM' ,26:'SUB' ,27:'ESC' ,28:'FS' ,29:'GS' ,30:'RS' ,31:'US',32:'SP' }
    def getVal(val):
        return chr(ASCII.charToVal[val])
    def getChar(val):
        return ASCII.valToChar[val]
    def getHumanPrint(lines):
        hp=""
        for line in lines:
            decType=ord(line)
            if  decType >= 0 and decType <=32:
                hp='%s[%s]'%(hp,ASCII.getChar(decType))
            else:hp='%s%s'%(hp,line)
        return hp
    def clearControlCharinLine(lines):
        hp=""
        for line in lines:
            decType=ord(line)
            if  decType >= 0 and decType <=32:
                continue
            else:hp+=line
        return hp

class SerialPort(object):
    "serial port lock eklenecek ve open closed kontrol edilecek."
    __slots__ = 'i','buffer','__lockFile','__RTSPIN','__rxbuf','__DEBUG', '__sparity', '__sstopbits', '__stimeout', 'meterRAWFile', '__readTimeOut', '__kapat', '__noReplay', '__serConnect', '__sport', '__defaultRawSave', '__busyExit', '__sbaud', '__sbyts', '__subprocess', '__opened', '__initiation','__useRtsCts'
    def __init__(self, port:int, sbaud:int, sbyts:int, DEBUG=0, meterRAWFile="/tmp/meterreader.raw",rawSave=False,busyExit=False,rxbuf=128,rts_pin='PA0',timeout=150):
        self.__DEBUG = DEBUG
        self.__sparity = 0 #Parity can be None, 0 (even) or 1 (odd)
        self.__sstopbits = 1 # Stop can be 1 or 2.
        self.__useRtsCts=True
        self.__stimeout = timeout
        self.meterRAWFile  = meterRAWFile
        self.__readTimeOut = 150
        self.__kapat = '%cB0%cq'%(1,3)
        self.__noReplay = "%cNo Replay to ? %c"%(1,3)
        self.__serConnect = None
        self.__sport = port
        self.__rxbuf = rxbuf
        self.__defaultRawSave=rawSave
        self.__busyExit=busyExit
        self.__RTSPIN= Pin(rts_pin,mode=Pin.OUT)
        if sbaud:
            self.__sbaud = sbaud
        else:
            self.__sbaud = 300
        if sbyts:
            self.__sbyts = sbyts
        else:
            self.__sbyts = 7
        self.__opened = False
        self.__initiation = False
        self.__lockFile='/flash/uartLock_%s'%(port)
        self.buffer=RINGBUFFER(rxbuf)
        self.i=0
        self.open()
    def __str__(self):
        msg="""
        Info SerialPort Port :%s Baud :%s  bytesize:%s parity :%s stopbits:%s opened :%s
        """%(self.__sport,self.__sbaud,self.__sbyts,
             self.__sparity,self.__sstopbits,self.__opened)
        return msg
    def rtsChange(self,val=False):
        if val:
            self.__RTSPIN.on()
        else:
            self.__RTSPIN.off()

    def getBuffer(self,index_get=None):
        if not index_get:
            index_get=self.buffer.index_get
        if index_get < self.buffer.index_put:
            return str(self.buffer.data[index_get:self.buffer.index_put].decode()).encode()
        elif index_get > self.buffer.index_put:
            return str('%s%s'%(self.buffer.data[index_get:self.buffer.size].decode(),self.buffer.data[:self.buffer.index_put].decode())).encode()
        else:
            return b''
    def open(self):
        while True:
            if not self.__initiation:
                try:
                    # SerialPort Open
                    self.__serConnect = self.__available_ttys(self.__sport,opened=self.__opened)
                    # self.__serConnect=machine.UART(1, baudrate=115384, bits=8, parity=None, stop=1, flow=0, timeout=0, timeout_char=2, rxbuf=64)
                    self.__serConnect=UART(self.__sport, baudrate= self.__sbaud, bits=self.__sbyts, parity=self.__sparity, stop=self.__sstopbits, flow=0, timeout=self.__stimeout, timeout_char=2, rxbuf=self.__rxbuf)
                    self.__opened = True
                    if self.__DEBUG > 5: print("initilized port:%s " % (self.__sport))
                    self.__initiation=True
                    with open(self.__lockFile,'w') as f:
                        f.write('%s'%self.__sport)
                        f.close()
                except Exception as e:
                    if self.__initiation:
                        if self.__opened:
                            self.__serConnect.close()
                    self.__opened = False
                    if self.__DEBUG > 2 and int(time()%3) == 0:
                        print("port:%s err:%s " % (self.__sport, e))
                    if self.__busyExit:
                        print('break')
                        break
                    sleep(1)
                    continue
            try:
                if not self.__opened:
                    self.baudrate(300)
                self.__opened = True
                break
            except Exception as e:
                if  self.__opened:
                    self.__serConnect.close()
                    self.__opened = False
                if self.__DEBUG > 2:print("err:%s" % e)
            sleep(int(time()%10))
        return True

    def close(self):
        if  self.__opened:
            self.__serConnect.deinit()
        try:
            os_remove(self.__lockFile)
        except Exception as e:
            print('%s err:%s'%(__name__,e))
        self.__opened = False
        return True

    def get_baudrate(self):
        return int(str(self.__serConnect).split(',')[1].split('=')[1])

    def baudrate(self, baud=None):
        if baud:
            self.__serConnect.init(baudrate=baud, bits=self.__sbyts, parity=self.__sparity, stop=self.__sstopbits, flow=0, timeout=self.__stimeout, timeout_char=2, rxbuf=self.__rxbuf)
            self.__opened=True
            self.__sbaud=baud
        else:
            return self.get_baudrate()

    def getport(self):
        return self.__sport

    def set_port(self,val):
        if "int" in str(type(val)):
            self.__serConnect.deinit()
            self.__sbaud=300
            self.__serConnect=UART(val, baudrate= self.__sbaud, bits=self.__sbyts, parity=self.__sparity, stop=self.__sstopbits, flow=0, timeout=self.__stimeout, timeout_char=2, rxbuf=self.__rxbuf)
        else:
            raise ValueError("str is not defined")
    def get_globaltimeout(self):
        return self.__readTimeOut

    def set_globaltimeout(self, t):
        if t > 0 and t < 500:
            self.__readTimeOut = t
        else:
            raise ValueError("0 < global timeiout <500")

    def __available_ttys(self, tty,opened=False):
            try:
                with open(self.__lockFile,'r'):
                    raise Exception('Port %s is busy ' % (tty))
            except Exception as e:
                if 'ENOENT' in str(e):
                    return tty
    def write(self, obis):
        if self.__DEBUG > 3:
            print("func=%s" % (self.write.__name__))
        try:
            logger.debug('W:%s'%ASCII.getHumanPrint(obis))
            if self.__useRtsCts:
                self.rtsChange(True)
            self.__serConnect.write(obis)
            if chr(6) in obis:
                self.set_globaltimeout( 5)
            elif self.__kapat in obis:
                self.set_globaltimeout(1)
            else:
                self.set_globaltimeout(60)
            if (self.__DEBUG > 2): print("Write :%s s_td:%d" % (ASCII.getHumanPrint(obis),self.get_globaltimeout()))
        except Exception as e:
            print("Obis :%s YAZILMADI err:%s" % (obis, e))
    def read(self):
        if self.__DEBUG > 3:print("func=%s" % (self.read.__name__))
        begin_index=self.buffer.index_put
        start = time()
        i=0
        state=False
        if self.__useRtsCts:
            self.rtsChange(False)
        # while self.buffer.getAndPutValue() == None or self.i ==begin_index:
        while True:
            try:
                self.buffer.put(ord(self.__serConnect.read(1)))
                i=0
            except Exception as e:
                # print(e)
                i += 1
            if 3 == self.buffer.getAndPutValue(index=-2) and i !=0: break #ETX
            if 21 == self.buffer.getAndPutValue(): break #NAK
            if 6  == self.buffer.getAndPutValue(): break #ACK
            if 10  == self.buffer.getAndPutValue(): break #ACK
            if (i > self.get_globaltimeout() or int(time() - start) > self.get_globaltimeout()):
                break
        logger.debug('R:%s td:%f'%(self.getBuffer(begin_index),time() - start))
        self.i=begin_index
        return self.getBuffer(index_get=begin_index)
    #wraper
    write_Serial=write
    read_Serial=read