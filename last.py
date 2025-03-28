noReg = 0
Gimei = "0"
Glocations = b''
timeStart = 0 
distance = 0 


apn = "m2m.tag.com"
PmodemPower = 26
PmodemPWRKey = 23
PmodemTx = 32
PmodemRx = 21
PmodemStatus = 22
PmodemDTR = 33
PmodemRing = 13

Psda = 18
Pscl = 19
PperipherialPower = 25
Pbuzzer = 27
Pinput14 = 14
Pinput4 = 4
Preed = 15
relay5V = 22


PGPSPwr = 16
pGPSRX = 17
pGPSTX = 17  


latitude = 0
longitude = 0
num_satellites = 0
altitude = 0
ground_speed = 0
timestamp_gps = 0



datalist = ['200','230','231','232','234','235','236','237','238','254','255','257','256','258','519','657']
defaults = ['421','422','587']
databaseParams = {"51":["W",0,0,0,"0","R"],"52":["E",9,2,"update()","0","R"],"53":["R",1,0,0,"0","R"],"54":["R",1,0,0,"0","R"],"55":["E",9,2,"downloadUpdate()","0","R"],"200":["R",1,0,0,"0","R"],"221":["E",9,2,"restart()","0","R"],"222":["E",9,2,"factoryReset()","0","R"],"230":["R",9,0,"1","0","R"],"231":["R",2,0,"1","0","R"],"232":["R",2,0,"1","0","R"],"234":["R",0,0,"1","0","R"],"235":["R",0,0,"1","0","R"],"236":["R",0,0,"1","0","R"],"237":["R",0,0,"1","0","R"],"238":["R",0,0,"1","0","R"],"254":["W",0,0,0,"0.00","W"],"255":["W",0,0,0,"0","W"],"257":["R",0,0,0,"0","R"],"290":["R",2,0,0,"0","R"],"312":["E",9,2,"get_settings()","0","R"],"421":["W",0,0,0,"60","R"],"422":["W",0,0,0,"300","R"],"427":["W",1,0,0,"100","W"],"429":["E",9,2,"resetCount1()","0","E"],"437":["R",2,0,0,"0","R"],"439":["R",2,0,0,"0","R"],"440":["R",1,0,0,"0","R"],"443":["R",0,0,0,"0","R"],"520":["R",0,0,0,"0","R"],"521":["R",0,0,0,"0","R"],"522":["R",0,0,0,"0","R"],"523":["W",0,0,0,"3.9","W"],"524":["W",0,0,0,"20","W"],"525":["W",0,0,0,"0","W"],"532":["R",0,0,0,"0","R"],"533":["R",0,0,0,"0","R"],"553":["W",0,0,0,"4","W"],"554":["W",0,0,0,"20","W"],"555":["W",0,0,0,"0","W"],"556":["W",0,0,0,"6","W"],"570":["R",0,0,0,"0","R"],"575":["W",0,0,0,"3.9","W"],"576":["W",0,0,0,"20","W"],"577":["W",0,0,0,"0","W"],"578":["W",0,0,0,"4","W"],"579":["W",0,0,0,"20",""],"580":["W",0,0,0,"0","W"],"581":["W",0,0,0,"6","W"],"582":["R",0,0,0,"0.00","R"],"587":["W",1,0,0,"10","W"],"593":["W",0,0,0,"12000","W"],"594":["R",0,0,0,"0","R"],"595":["R",0,0,0,"0","R"],"636":["W",0,0,0,"1","W"],"637":["W",0,0,0,"1","W"],"638":["W",0,0,0,"1","W"],"639":["W",0,0,0,"1","W"],"640":["W",0,0,0,"0","W"],"641":["E",9,2,"limit2G()","0","R"],"642":["E",9,2,"limit4G()","0","R"],"643":["E",9,2,"limitNB()","0","R"],"644":["E",9,2,"limitCatM()","0","R"],"645":["E",9,2,"limitOFFI()","0","R"],"214":["W",1,0,0,"240","W"],"256":["R",2,0,0,"0","R"],"258":["R",2,0,0,"0","R"],"519":["R",2,0,0,"0","R"],"657":["R",0,0,0,"0","R"]}
firmwareVersion = "1_0_0"
import time
import utime
import gc
import machine
from machine import mem32
import struct
import json
import network
import btree
from machine import Pin, UART
import re
import _thread
import gc



wakeCause = "Unknown"
resetCause ="Unknown"
causeSent = False
errors = "" 
errorsSent = True
connectionSuccess = False

registrationStart = utime.time()
registrationTime = 0
timestamp = 0
winame = "none"

this_antenna = None

class GPS:
    def __init__(self, tx_pin=17, rx_pin=17):
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.num_satellites = 0
        self.ground_speed = 0
        self.timestamp_gps = 0
        self.timestring = None
    
        
    def turn_on_gps(self):
        
        print("Turning ON GPS")
        self.uart = UART(1, 115200, tx=pGPSTX, rx=pGPSRX, parity=None, stop=1)
        power_pin = machine.Pin(PGPSPwr, machine.Pin.OUT, machine.Pin.PULL_UP)
        power_pin.value(1)
        time.sleep(1)

    def read_gps_data(self):
        power_pin = machine.Pin(PGPSPwr, machine.Pin.OUT, machine.Pin.PULL_UP)
        power_pin.value(1)
        self.uart = UART(1, 115200, tx=pGPSTX, rx=pGPSRX, parity=None, stop=1)
        sentence_buffer = bytearray()
        time.sleep(1)
        ttime = time.time()
        
        try:
            #while True:
             #   if (time.time()- ttime) > 8:
              #      break
            if self.uart.any():
                char = self.uart.read()
                sentence_buffer += char
                if sentence_buffer.endswith(b"\r\n"):
                    self.parse_sentence(sentence_buffer)
                    sentence_buffer = bytearray()  # Изчистваме буфера
                        
        except KeyboardInterrupt:
            sys.exit(0)

    def parse_sentence(self, sentence_buffer):
        global latitude
        global longitude
        global num_satellites
        global altitude
        global ground_speed
        global timestamp_gps
        
        try:
            decoded_sentence = sentence_buffer.decode('utf-8').strip()
        except Exception as e:
            print("")
            return
            
        #print(decoded_sentence)
        
        if decoded_sentence.startswith("$GNGGA"):  
            parsed_data = decoded_sentence.split(',')
                
            if len(parsed_data) >= 10:
                if len(parsed_data[7]) > 0 and len(parsed_data[9]) > 0 and len(parsed_data[2]) > 0 and len(parsed_data[4]) > 0:
                    
                    num_satellites = parsed_data[7]  
                    altitude = parsed_data[9]
                        
                    self.latitude = parsed_data[2]
                    latP = parsed_data[3]
                    self.longitude = parsed_data[4]
                    lonP = parsed_data[5]
                        
                        
                    if len(self.latitude) >= 4:
                        latdeg = int(self.latitude[0:2])
                        latmin = float(self.latitude[2:])
                        self.latitude = latdeg + latmin/60
                        if latP == "S" :
                            self.latitude = self.latitude * -1
                            self.latitude = round(self.latitude,6)
                        latitude = round(self.latitude, 6)
                        
                    if len(self.longitude) >= 5:
                        londeg = int(self.longitude[0:3])
                        lonmin = float(self.longitude[3:])
                        self.longitude = londeg + lonmin/60
                        if lonP == "W" :
                            self.longitude = self.longitude * -1
                            self.longitude = round(self.longitude,6)
                        longitude = round(self.longitude, 6) 
        
        elif decoded_sentence.startswith("$GNRMC"):
            parsed_data = decoded_sentence.split(',')
            if len(parsed_data) >= 10:
                
                if float(parsed_data[7]) > 0:    
                    ground_speed = round(float(parsed_data[7])*1.852,2)
                
                if len(parsed_data[1]) > 0 and len(parsed_data[9]) > 0:
                    self.timestring = parsed_data[1]
                    dstring = parsed_data[9]
                    dstring = str(dstring)
                    yearString = int("20" + dstring[4:6])
                    monthString = int(dstring[2:4])
                    date = int(dstring[0:2])
                        
                    h =int(self.timestring[0:2])
                    m =int(self.timestring[2:4])
                    s =int(self.timestring[4:6])
                    
                    t = (yearString,monthString,date,h,m,s,0,0)
                    timestamp_gps = utime.mktime(t) + 946684800
                        #print("timestamp_gps =", self.timestamp_gps)
                    
buff = bytearray()

class Antenna:
    def __init__(self):
        self.antenna_count = {}  
        po = Pin(25, Pin.OUT)
        po.value(1)
        
    def process_packets(self):
        uart = UART(2, baudrate=115200, tx=13, rx=39, timeout=1)
        global buff
        MAX_BUFFER_SIZE = 2048
        
        while True:
            try:
                if uart.any():
                    data = uart.read()
                    #print("data:", data)
                    if data:
                        #if len(buff) + len(data) <= MAX_BUFFER_SIZE:
                         #   buff.extend(data)
                        #else:
                        buff.extend(data)
                        
                        self.parse_buffer()  # Обработка на буфера
                            #buff = bytearray()  # Изчистване след обработка
                          # Добавяне на новите данни

                time.sleep(0.150)
                gc.collect()  # Освобождаване на паметта при нужда
            
            except Exception as e:
                print("Error", str(e))




        
                
    def parse_buffer(self):
        global buff
        global latitude
        global longitude
        global num_satellites
        global altitude
        global ground_speed
        global timestamp_gps
        #print("da1")
        while b'\r\n' in buff:
            #print("da2")
            packet, buff = buff.split(b'\r\n', 1)
            try:
                packet_str = packet.decode('ascii').replace(' ','').replace('\n', '').replace('\r', '')
                print("pachet_str:", packet_str)
            except Exception as e:
                print("Error decode:", e)
            #print("da3")
            parts = packet_str.split(',')
            if len(parts) >= 4:
                print("parts[3]", parts[3])
                antenna_serial = parts[3]
                antenna_serial = antenna_serial[:24]
                if len(antenna_serial) != 24:
                    #relay5 = machine.Pin(relay5V, machine.Pin.OUT)
                    #relay5.value(1)
                    #time.sleep(2)
                    #relay5.value(0)
                    #time.sleep(10)
                    continue
                
                if antenna_serial in self.antenna_count:
                    self.antenna_count[antenna_serial]['count'] += 1
                else:
                    
                    self.antenna_count[antenna_serial] = {
                        'count': 1, 
                        'data': {
                            'latitude': latitude,
                            'longitude': longitude,
                            'num_satellites': num_satellites,
                            'altitude': altitude,
                            'ground_speed': ground_speed,
                            'timestamp_gps': timestamp_gps
                        }
                    }
                    

    def print_antenna_counts(self):
            counter = 0
            for antenna, count in self.antenna_count.items():
                counter += 1
                print(f"Антена: {antenna}, Прочетена пъти: {count['count']}")
            print("Всички прочетени антени: ", counter)
            
def wdtAlert(p):
    print("WDT Reset")
    db.store()
    modem.turnOff()
    machine.reset()
    wdt = machine.Timer(10)
    wdt.init(period=440000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)

class sim7070(object):
    
    
    def __init__(self):


        #,power,key,tx,rx,br
        #self.pwr = machine.Pin(power,machine.Pin.OUT)

        
        
        self.tx = PmodemTx
        self.rx = PmodemRx
        self.br = 9600
        self.apn = apn


        
        self.pwr = machine.Pin(PmodemPower,machine.Pin.OUT)
        self.status = machine.Pin(PmodemStatus, machine.Pin.IN)
        self.dtr = machine.Pin(PmodemDTR, machine.Pin.OUT)
        self.ri = machine.Pin(PmodemRing, machine.Pin.IN)
        

        
        self.dtr.value(0)
        return


    def isOn(self):
        self.uart = machine.UART(1,self.br, rx=self.rx, tx=self.tx, txbuf=1024,rxbuf=2048)
        self.us("AT")
        
        at = self.us("AT")
        if type(at)  != bytes and type(at) != str:
            return False
        self.us('AT+CNCFG=0,1,"'+self.apn+'"')
        if  "OK" in at:        
            return True
        else :
            return False
        
    def turnOn(self):
           
        #self.pwr.value(0)
        
        
        if self.isOn() == False:


            
            
            
            #machine.Pin(PmodemPWRKey,machine.Pin.IN,machine.Pin.OUT).value(0)
            machine.Pin(PmodemPWRKey,machine.Pin.OUT).value(0)
            
            time.sleep(2)
            
            machine.Pin(PmodemPWRKey,machine.Pin.OUT).value(1)
            #machine.Pin(PmodemPWRKey,machine.Pin.IN,machine.Pin.OUT).value(1)
            time.sleep(6)
            self.us("AT",0.5)
            self.us("AT",0.5)
            
            x = 0
            time.sleep(1)
            #self.us('AT+COPS=1,2,"28401",9',2)
            #self.limitOFF()
            self.us('AT+CNCFG=0,1,"'+self.apn+'"',1)
            self.us('AT+CCID')
            self.us('AT+CNCFG=0,1,"'+self.apn+'"',1)
            #self.limitCatM()
            
            if self.isReg():
            
                
                self.us('AT+CNCFG=0,1,"'+self.apn+'"')
            else:
                #self.us('AT+COPS=1,2,"28401",9',2)
                #self.us('AT+COPS=1,2,"28405",7',1)
                while x <0 :

                    if self.isReg():
                        time.sleep(1)

                        self.us('AT+CNCFG=0,1,"'+self.apn+'"')
                        return
                    else:
                        time.sleep(1)
                    x = x+1
                #self.us("AT+CMCFG=1")
                #self.us("AT+CNMP=51")
                #self.us("AT+CMNB=1")
                #self.us("AT+CCID")

            return True
        

    def turnOff(self):
        
        
        
        try: 
            #self.us("AT+CFUN=0")
            #time.sleep(2)
            self.us("AT+CPOWD=1")
            
            time.sleep(2)
            #self.pwr.value(0)
            return True#self.pwr.value()
        except :
            return False
        #else :
        #    return True
    def sleep(self):
        self.dtr.value(1)
    def wakeUp(self):
        self.dtr.value(0)

    def limitNB(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=2")
        self.us("AT+CFUN=0")
        time.sleep(2)
        self.us("AT+CFUN=1")

    def limitCatM(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=1")
        self.us("AT+CFUN=0")
        time.sleep(2)
        self.us("AT+CFUN=1")

    def limit4G(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=3")
        self.us("AT+CFUN=0")
        time.sleep(2)
        self.us("AT+CFUN=1")

    def limit2G(self):
        self.us("AT+CNMP=13")
        self.us("AT+CFUN=0")
        time.sleep(2)
        self.us("AT+CFUN=1")

    def limitOff(self):
        self.us("AT+CNMP=2")
        self.us("AT+CMNB=3")
        self.us("AT+CFUN=0")
        time.sleep(2)
        self.us("AT+CFUN=1")

    def registerNetwork(self):
        if self.isReg():
            return True
        else:
            #First timer
            registrationStart = utime.time()
            
            while utime.time() - registrationStart  < 300:
                wdt = machine.Timer(10)
                wdt.init(period=300000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                print("Reg timer 1 - remembered from previous session")
                if self.isReg():
                    return True
                else :
                    utime.sleep(1)
           
            #self.us("AT+CNMP=51")
            #self.us("AT+CMNB=3")
            #self.turnOff()
            #self.turnOn()
            self.limitOff()
            self.us("AT+COPS=0")
            self.us("AT+CFUN=0")
            self.us("AT+CFUN=1")
            return False


    def isReg(self):

        global noReg 
        noReg = 0 
       # return True
        if self.isOn() == False: 
            print("Modem was not ON. Turning ON...")
            self.turnOn()
            return False
        if self.us("AT",0.2) is not None :
            cpsi =  self.us('AT+CPSI?',0.2)
            if  'Low Power Mode' in cpsi:
                self.us("AT+CFUN=1")
            if  'NO SERVICE' in cpsi:
                noReg += 1
                return False
            elif 'AT+CPSI' in cpsi:

                noReg = 0 
                return True
            else : 
                return False
            
        else :
            print("None from isReg()")
            if self.isOn():
                return False
            else : 
                self.turnOff()
                self.turnOn()
                return False
                


    def getImei(self):
        self.us('AT+CGDCONT=1,"IP","'+apn+'"')
        self.us("AT")
        self.us("AT+CRATSRCH=2,2",1)
        imei = self.us("AT+GSN").decode("utf-8")
        imei = imei.replace("AT+GSN","")
        imei = imei.replace("\r","")
        imei = imei.replace("\n","")
        imei = imei.replace("OK","")
        return imei
    def getCCID(self):
        self.us("AT")

        ccid = self.us("AT+CCID").decode("utf-8")
        ccid = ccid.replace("AT+CCID","")
        ccid = ccid.replace("\r","")
        ccid = ccid.replace("\n","")
        ccid = ccid.replace("OK","")
        return ccid
    def getBat(self):
        self.us("AT")
        bat = self.us("AT+CBC").decode("utf-8")
        bat = bat.replace("AT+CBC","")
        bat = bat.replace("\r","")
        bat = bat.replace("\n","")
        bat = bat.replace("OK","")
        bat = bat.replace("+CBC: ","")
        spl = bat.split(",")
        
        
        #self.fillEng()
        return spl


    
    def getTimeF(self):
        self.us("AT")
        self.connectHiGPS(1)
        tim = self.sendHiGPS("/t/")
        try:
            return tim.decode("utf-8")
        except:
            return False
    def getCPSI(self):
        
        eng =  self.us("AT+CPSI?",1.5).decode("utf-8")
        ee = eng.split("CPSI: ")
        self.us("AT+CENG=0")
        eng = ee[1]
        eng = eng.replace("\r","")
        eng = eng.replace("\n","")
        eng = eng.replace("+","")
        eng = eng.replace(" ",";")
        return eng
    def connectHiGPS(self,num): 
            global registrationTime
            global registrationStart
                
            connected = False
            retry = 6
            
            registrationTime = utime.time() - registrationStart
            print("registration time = ",registrationTime)
            cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
            while "0,ACTIVE"  not in cnact  and retry >0 :
                deact = self.us('AT+CNACT=0,0',2)
                cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
                retry = retry -1 
            if "DEACTIVE" in cnact and '0,ACTIVE' not in cnact:      
                self.restart()          
                #self.turnOff()
                #self.turnOn()
                self.registerNetwork()


            
    def getData(self,response,cid):
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 7,*SET,55', '', 'OK', '']
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 0', '', 'OK', '', '+CADATAIND: 0', '', '+CASTATE: 0,0', '']
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 5,15858', '', 'OK', '']
        
        resp = response.split(b'\r\n')
        n = 0
        for repons in resp : 
            if repons == b'AT+CARECV='+str(cid)+b',512\r':
                break 
            else:
                n +=1


        
        if len(resp)>0:
        
            datalen =  int(resp[n+1][9:].split(b',')[0])
            print("Data len = ",datalen)
        else:
            return False

        ind = response.index(b'+CARECV: ')
        start = ind+10+len(str(datalen))
        end = start+datalen
        inp = response[start:end]

        return inp

    def sendHiGPS(self,message):
        message = message.replace('"','')
        print("modem.sendUDP message:" )
        print(message)
        self.us("AT+CNACT?",1)
        cid = 0
        timeout = 30
        connectionOpened = False
        openResult = self.us('AT+CAOPEN='+str(cid)+',0,"TCP","in.higps.org",80')
        while timeout >0 and cid < 13:
            if  type(openResult) == bytes and b'CAOPEN: '+str(cid)+',0' in openResult:
                print("Connection Opened")
                connectionOpened = True
                timeout = 30
                break
            elif type(openResult) == bytes and ( b'CAOPEN: '+str(cid)+',1' in  openResult or "ERROR" in openResult):
                print("Connection Failed")
                cid +=1
                openResult = self.us('AT+CAOPEN='+str(cid)+',0,"TCP","in.higps.org",80',1)
            else: 
                print("Waiting for connection")
                openResult = self.us("AT",1)
            timeout = timeout -1
        if connectionOpened == False:
            print("Unable to open connection within timeout")
            return False

        sendResult = self.us('AT+CASEND='+str(cid)+','+str(len(message)+6),1)
        if "ERROR" in sendResult:
            return False
        self.us('GET '+message+'\r\n')
        self.us('AT+CAACK='+str(cid),1)
        resp = self.us('AT+CARECV='+str(cid)+',512',1.5)
        print(resp)
      
        print("resp")
        print(resp)
        try: 
            toret = self.getData(resp,cid)
            print("Toret = " ,toret)
            if toret == False or toret == b'':
                time.sleep(1)
                resp = self.us('AT+CARECV='+str(cid)+',512',1.5)
                print("Retry read")
                toret = self.getData(resp,cid)
            self.us('AT+CACLOSE='+str(cid))
            return toret
        except: 
            return False
    def cipClose(self):
        

        self.us("AT+CNACT=0,0")
    def restart(self):
        self.us("AT+CFUN=0",2)
        time.sleep(1)
        self.us("AT+CFUN=1",2)    
    def us(self,arg,t=0):
        
        #print(arg)
        answer = []
    
        self.uart.write(arg)
        self.uart.write(bytes([0x0d,0x0a]))
        time.sleep(0.1)
        time.sleep(t)
        answer = self.uart.read();
        
        print(answer)
        if hasattr(answer,"decode"):
            return answer
        else:
            return "False"

class database(object): 
    def __init__(self):
        
        
        
        self.newdata = False
        global databaseParams
        #key = higpsID
        #param[0] = Allowed operations - R (read), W (read-write), E (execute)
        #param[1] = Type: 1 - number, 0 - string, 2 - boolean, 3- buffer 9 - function
        #param[2] = Storage: 0 - file system, 1 - RAM, 2 - Function 
        #param[3] = Path = 0 - default / function name
        #param[4] = Default value
        
        database.params = databaseParams
        try:
            try:
                f = open("mydb", "r+b")
            except OSError:
                f = open("mydb", "w+b")        
            db = btree.open(f)
            self.data = {}
            for key in db:
                #if data[key][1] == 0
                #if key
                self.data[key] = db[key]

            db.flush()
            db.close()
            f.close()
        except Exception as e:
            setError(" Error in Database "+(str(e)))

            return False
            
            

    def getParameterData(self,uri):
        try:
            #if 
            return self.params[uri]
        except:
            return False
    
    def getParameterByHiGPS(self,higpsId):
        print("in get parameter by HiGPS")
        print(higpsId)
        try:
            return self.params[higpsId]
        except:
            return False   



    def initDefaults(self):
        import os
        if len(self.data) > 0:
            os.remove('mydb')
        
        
        
            print("old db removed")
            utime.sleep(5)
            machine.reset()
        else:
            print("no previous DB ")
        n = 0
        imei = '2111111111111'
        while n< 3 and len(imei) != 15:  
            imei = modem.getImei()
            n +=1

        
        self.newdata = True
        for higpsID in self.params:
            if self.params[higpsID][4] != None and self.params[higpsID][2] == 0:
                if higpsID == "200":
                    self.write(higpsID,imei)    
                else:
                    self.write(higpsID,self.params[higpsID][4])



    def read(self,property,echo=True):
        
        praw = property

        try:
            if type(property) == str :
                property = str.encode(property)
            if echo:
                print("Reading "+str(property)+ " = " + str(self.data[property]))
            if property in self.data:
                return self.data[property]
            elif praw in self.params:
                return self.params[praw][4]
            else : 
                return False
            

        except Exception as e:
            #print(e)
            return False

    def write(self,property,value):
        self.newdata = True
        try:
            if type(value) == int: 
                value = str(value)
            if type(value) == str:
                value = str.encode(value)
            if type(property) == str:
                property = str.encode(property)
            print("Writing "+str(property)+ " = " + str(value))
            self.data[property] = value

            return True
        except:
            return False
    def store(self):
        if self.newdata == False:
            print("No data to write")
            return True


        #try:
        
        print("Database store started")
        try:
            f = open("mydb", "r+b") 
        except OSError:
            f = open("mydb", "w+b")
        db = btree.open(f)

        for key in self.data:
            if len(key) <= 3: 
            #Buffer Handling 
                db[key] = self.data[key]

                if key.decode('utf-8') in self.params and self.params[key.decode('utf-8')][1] == 3:
                    #print("In buffer")
                    n = 0
                    while n< 100: 
                        #print("Buffer n ",n)
                        key_child = key+str(n)
                        if key_child in self.data and len(self.data[key_child]) > 0:
                            #print("Storing child ",key_child)
                            db[key_child] = self.data[key_child]
                        n +=1
                #elif self.params[key.decode('utf-8')][2] == 0:
                    
                    
        db.flush()
        db.close()
        f.close()
        print("Database store completed")
        return True
        #except Exception as e:

         #   print("Failed writing in database ",e)
          #  return False
        
class buffer(object):

    def create(bufferName):
        #data = b'\x00'
        print("In create")
        timestamp = device.getTimestamp()
        print("Timestamp ", timestamp)

        period = int(db.read('421'))
        print("Period ", period)
        data = struct.pack("H", period)
        data += struct.pack("L", timestamp)
        if bufferName == "540":             
            data +=  struct.pack('L',int(db.read('437')))
        elif bufferName == "541": 
            data +=  struct.pack('L',int(db.read('439')))
        print("Sturct Data ",data)
        #data = period.to_bytes(2,'big')+timestamp.to_bytes(4,"big")
        c=0 
        done = False
        while  c< 100:
            buff = bufferName + str(c)
            currentBuffer = db.read(buff)
            if currentBuffer == False  or len(currentBuffer) < 2 : 
                #Empty buffer
                db.write(buff,data)
                done = True
                break 
            c+=1
        if done == False: 
            buff = bufferName + "0"
            db.write(buff,data)
            c = 0 
        if bufferName == '540':
            db.write("538",str(c))
        elif bufferName == '541': 
            db.write("539",str(c))

        return c

    def get(bufferName):

        c =0 
        while c < 100 : 
            buff = bufferName + str(c)
            buffData = db.read(buff)

            if buffData and len(buffData) > 10: 
                #Full buffer
                print("Buffer found ", c)
                print("Buffer data ", buffData)
                 
                #timestamp = buffData[]
                period = struct.unpack("H",buffData[0:2] )
                timestamp = struct.unpack("L", buffData[2:6] )
                baseValue = struct.unpack("L", buffData[6:10] )
                data = buffData[10:]
                print("Period ",period)
                print("Timestamp ",timestamp)
                return (period[0],timestamp[0],baseValue[0],data)

            c +=1
        return False


    
    def put(bufferName,data):
        if bufferName == '540':
            c = db.read("538").decode('utf-8')
        elif bufferName == '541': 
            c = db.read("539").decode('utf-8')

        buff = bufferName + str(c)
        print("Buffer ready ",c)
        buffData = db.read(buff)
        if buffData != False:
            bufferData = buffData + data
            db.write(buff,bufferData)
        
        
    def remove(bufferName):
        c =0 
        while c < 100 : 
            buff = bufferName + str(c)
            buffData = db.read(buff)

            if buffData and len(buffData) > 10 : 
                #Full buffer
                print("Buffer to remove ", c)
                print("Buffer data ", buffData)
                db.write(buff,"0")                 
                
                return True

            c +=1
        return False
        

class findyIoT(object):
    def __init__(self):
        
        
        findyIoT.requestType = ""
        findyIoT.responceType = ""
        #higps.modem = modem #sim7000(26,23,32,21,9600)
        findyIoT.imei = Gimei
        


        #higps.modem.isOn()
    def main(self,command,execute = True):
        
        global lastReportTime
        while command:
            command = self.send(command,execute)

            
        lastReportTime = utime.time()
        print("Last report was on ")
        print(lastReportTime)
        return command
    def send(self,commandtype,execute):
        
        global lastReportTime
        global errors
        global errorsSent
        global connectionSuccess
        global registrationTime
        global timestamp
        global firmwareVersion
        global timeOffset
        connectionSuccess = False
        if "," in commandtype :
            spl = commandtype.split(",")
            commandtype = spl[0]
            parameter  = spl[1]
            symbols = {"self": self,"parameter" : parameter}

            data = eval("self.get_"+commandtype+"(parameter)", symbols)
        else: 
            symbols = {"self": self}   
            data = eval("self.get_"+commandtype+"()", symbols)
        modem.connectHiGPS(2)
        
        response = modem.sendHiGPS('/input.php?'+data+"&er="+errors.replace(' ','%')+"&rt="+str(registrationTime)+"&t=1&fw="+firmwareVersion)
        #timestamp = modem.sendHiGPS('/t/')
        #print(timestamp)
        #modem.cipClose()
        print("Response in send")
        print(response)
        if response == False:
            print("retry")
            modem.restart()
            #modem.turnOff()
            #modem.turnOn()
            if modem.isOn():
                if modem.registerNetwork():
                    modem.connectHiGPS(2)
                    response = modem.sendHiGPS('/input.php?'+data+"&t=1")#+"&error="+errors.replace(' ','%'))
            
        

        
        
        if response:
            response = response.decode("utf-8")
            connectionSuccess = True
            print("SENT OK") 
            
            errorsSent = True
            errors = ""
            command = self.parse(response)
            #if len
            #global wdt
            #wdt.feed()

            print(command)
            # ok
        else : 
            command = False


        print(command)
        if execute and command == False and response != False and len(response) == 10 :
            timestamp = response
            print(response)
            #decodedTs = response.decode("utf-8")
            if len(response) == 10: 
                timeDevice =device.getTimestamp()
                ttt=time.localtime(int(response)-946684800)

                machine.RTC().init((ttt[0],ttt[1],ttt[2],0,ttt[3],ttt[4],ttt[5],0))
                timeServer = device.getTimestamp()
                print("Time Device ", timeServer) 
                timeOffset = timeServer - timeDevice
                print("Time Offset ",timeOffset)


                print(machine.RTC().datetime())
        modem.cipClose()
        if command  and execute :

            symbols = {"self": self,"data": response} 
            return eval("self.set_"+command+"(data)", symbols)
        #else:
        #    return command

   
    def parse(self,rsp) :

        #from machine import WDT
        #wdt = WDT(timeout=2000)  # enable it with a timeout of 2 seconds
        #wdt.feed()
        
        
        if "#" in rsp :
            
            if "#User=" in rsp : 
                parsed = "user"
            elif "#+" in rsp : 
                parsed ="phones"
            else :
                parsed =False
        elif "*" in rsp:

            if "*MODE-" in rsp : 
                parsed ="mode"
            elif "*MODE?$" in rsp : 
                parsed ="modeQ"
            elif "*GPRS$" in rsp : 
                parsed ="gprs"
            elif "*GSM$" in rsp : 
                parsed ="eng"
            elif "*WIFI$" in rsp : 
                parsed ="wifi" 
            elif "*START" in rsp :     
                parsed ="start" 
            elif "*STOP" in rsp :     
                parsed ="stop" 
            elif "*SET" in rsp: 
                parsed = 'set' 
            elif "*GET" in rsp: 
                parsed = 'get' 
            else : 
                parsed =False
        else : 
            parsed = False
            #       print(parsed)
        return parsed

    def set_set(self,response):
        print(response)
        #response = response.decode("latin-1", 'ignore')
        response = response.replace('$','')
        splitted = response.split(",")
        if len(splitted) == 2 : 
            print("Execute command")
            print(splitted[1])
            parameterData = db.getParameterByHiGPS(splitted[1])
            print(parameterData)
            if(parameterData[0] == "E"):
                
                
                print(parameterData[3])
                
                #eval("device.device.memoryTotal()")
                eval("self."+parameterData[3])
                #return "command,"+str(splitted[1])

            #execute
        elif len(splitted) == 3 :
            print("Write setting" + splitted[1] +" = "+ splitted[2])
            parameterData = db.getParameterByHiGPS(splitted[1])
            if(parameterData[0] == "W"):
                print(parameterData[0])
                
                db.write(splitted[1],splitted[2])
           
                db.store()
                return "setting,"+str(splitted[1])

        else : 
            return False
    def set_get(self,response):
        #response = response.decode("latin-1", 'ignore')
        response = response.replace('$','')
        splitted = response.split(",")
        
        print("Get Measurement" + splitted[1])
        parameterData = db.getParameterByHiGPS(splitted[1])
        if parameterData[0] == "W" or  parameterData[0] == "R":
            value = db.read(splitted[1])
                
            return "setting,"+str(splitted[1])

        else : 
            return False

    def get_defaults(self): 
        global defaults
            
        
        try:
            bat= modem.getBat()
        except:
            bat= modem.getBat()
        batPercent  = str(bat[1])
        message =  "IMEI="+str(Gimei)+"&bat="+batPercent+"&data="+self.get_data(defaults)
        return message
    def get_samplings(self):
        #global wakeCause
        #global resetCause
        #global causeSent 
        #global datalist
        try:
            bat= modem.getBat()
        except:
            bat= modem.getBat()
        batPercent  = str(bat[1])
        batVolt  = str(bat[2])
        #datalist = ['443','421']
        global datalist
       

        message =  "IMEI="+str(Gimei)+"&bat="+batPercent+"&data="+self.get_data(datalist)
        return message
    def get_samplingsAlarm(self):
        
        return self.get_samplings()+"440,1;"
    def get_dataBat(self):
        global Gimei
        try:
            bat= modem.getBat()
        except:
            bat= modem.getBat()
        
        batPercent  = str(bat[1])
        batVolt  = str(bat[2])
        message = 'IMEI='+str(Gimei)+'&bat='+batPercent+'&batVolt='+batVolt

        return message
    def get_data(self,datalist):
        import ubinascii
        
        data = ""


        for par in datalist:
            if par in db.params:

                print(par)
                
                if par == '594' or par =='595':
                        raw = db.read(par)    
                        print(raw.split(b'\xff\xff'))
                        value = "["
                        for val in raw.split(b'\xff\xff'):
                            try: 
                                num = struct.unpack('f',val)
                                print(num)
                                value += str(num[0])
                                value += ":"
                            except:
                                print("Except ", val)
                                if val != b'':
                                    value += ":"

                        value = value[:-1] + "]"
                elif par == '540' or par == '541':
                    raw = buffer.get(par)

                    print("RAW BUFFER ", raw)
                    if raw:
                        period = raw[0]
                        timestamp = raw[1]
                        initialValue = raw[2]
                        bufferData = raw[3]

                        #raw.split(b'\xff\xff')
                        value = "["
                        #raw.split(b'\xff\xff')
                        #decodedList = []
                        numBytes = len(bufferData)
                        for i in range(0, numBytes, 2):
                            #decodedList.append(int.from_bytes(encodedBytes[i:i+2], 'big'))
                            value += str(int.from_bytes(bufferData[i:i+2], 'big'))
                            value += ":"
                        value = value[:-1] + "]"
                        value += ";t_"+par+","+str(timestamp)
                        value += ";p_"+par+","+str(period)
                        value += ";i_"+par+","+str(initialValue)

                else:                    
                    value = db.read(par).decode("utf-8")
                if value: 
                    value=value
                else :
                    value=""

                data += par+","+value+";"
        
        return data
    def get_setting(self,id):
        parameterData = db.getParameterByHiGPS(id)
        if parameterData[0] == "W" or parameterData[0] == "R":
            datalist = [id]
            message = "IMEI="+str(Gimei)+"&set="+self.get_data(datalist)
            print(message)
            return message
    def get_command(self,id):
        parameterData = db.getParameterByHiGPS(id)
        if parameterData[0] == "E":
            datalist = [0]
            message = "IMEI="+str(Gimei)+"&set="+id
            print(message)
            return message
    def downloadUpdate(self):
        #55
        
        
        
        
        wdt = machine.Timer(10)
        wdt.init(period=60000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
        print("starting Download")
        downloadImage = db.read('51')
        if downloadImage != b'':
            print(downloadImage)
            downloadImage = downloadImage.decode("utf-8")
            db.write('53','1')
            db.write('54','0')
            self.main("setting,53",False)
            
            modem.connectHiGPS(2)
            fileSize = modem.sendHiGPS('/repo/'+str(downloadImage))
            modem.cipClose()
            print(fileSize)
            fileSize = fileSize


            n = 0
            a = True
            resp = ""
            if n ==0 :
                f = open( 'new.mpy', 'w' )
                f.write( "" )
                f.close()
            frames = 0
            
            while a == True :
                wdt.init(period=90000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                #wdt = machine.Timer(10)
                #wdt.init(period=360000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                modem.connectHiGPS(2)
                resp = modem.sendHiGPS('/repo/'+str(downloadImage)+'/512/'+str(n))
                time.sleep(2)
                part2 = modem.uart.read()
                if resp != None:
                    if part2 != None:
                        decodedResp = resp+part2
                    else:
                        decodedResp = resp
                print(decodedResp)
                modem.cipClose()
                


                totalSize = int(fileSize)
                frames = int(totalSize/512)
                if totalSize == frames*512:
                    frames = frames-1
                print("Total packets in the package = ") 
                print(totalSize)
                print("Number of frames")
                print(frames)
                print("Current frame") 
                print(n)
                
                print("checkpoint1")
                if n == frames :
                    f=open("new.mpy", "a")
                    f.write(decodedResp)  
                    f.close()
                    import os 
                    fsize=os.stat("new.mpy")
                    print("File size =") 
                    print(fsize[6])
                    if fsize[6] == totalSize:
                        wdt.init(period=90000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                        db.write('53','2')

                        self.main("setting,53",False)
                        time.sleep(1)
                        self.main("setting,54",False)
                        time.sleep(1)
                        print("finishing download")
                        self.main("command,55")        
                        a = False
                    else:
                        db.write('53','0') 
                        self.main("setting,53",False)
                        db.write('54','7')
                        self.main("setting,54",False)
                        return False


                print("checkpoint2")
                if decodedResp != False :
                    print("checkpoint3")
                    print(len(decodedResp))
                    if(len(decodedResp) == 512):
                        n = n+1 
                        f = open("new.mpy", "a")
                        f.write(decodedResp)  
                        f.close()

        return True
    def update(self):
        import gc
        import os
        gc.collect()
        #52
        print("Updating Firmware")
        db.write('53','0')
        
        db.write('54','1')
        self.main("setting,53",False)
        self.main("setting,54",False)
        try: 
        #            import new
            gc.collect()

            os.rename('new.mpy','last.mpy')
            self.main("command,52",False)
            
            time.sleep(3)
            machine.reset()
        #device.device.update()
        except Exception as e:
            print("Exception !!! ")
            print(e)
            os.remove('new.mpy')

        
        return True      
    def resetCount1(self):
        timestamp = device.getTimestamp()
        #modem.turnOff()

        counter.initCounter()
        modem.restart()
        #modem.turnOn()        
        modem.registerNetwork()
        #db.write('443',timestamp)
        self.main("command,429")
        #device.resetValGyro(self.db)
        return True

    def updateTime(self):
        device.getTimestamp()
        self.main("command,8")
    def serialNumber():
        self.main("setting,"+str(device.serialNumber()))
        return True
    def restart(self):
        
        self.main("command,221",False)
        
        machine.reset()
        return True
    def factoryReset(self):
        self.main("command,222",False)
        device.factoryReset()
        return True
    def limit2G(self):
        self.main("command,641",False)
        modem.limit2G()
        machine.reset()
        return True
    def limit4G(self):
        self.main("command,642",False)
        modem.limit4G()
        machine.reset()
        return True
    def limitNB(self):
        self.main("command,643",False)
        modem.limitNB()
        machine.reset()
        return True
    def limitCatM(self):
        self.main("command,644",False)
        modem.limitCatM()
        machine.reset()
        return True
    def limitOFF(self):
        self.main("command,645",False)
        modem.limitOff()
        machine.reset()
        return True

    
class counter(object):

    def valFromMem(val):
        
        from machine import mem32
        return (mem32[val] &  0xFFFF)//2


    def printAllSamplings():
        from machine import mem32
        aa = 0x500002a0
        #the addition of 8 is to keep a visible guard area
        io4 = []
        io14 = []
        even = True
        while aa < ( 0x500002a0 + ( (0x168 - 0x10)*4)) :

            print(str(hex(aa)) + " = "+ hex(mem32[aa]))
            aa +=4

    def getSamplings():
        

        
        ulp_edge_count = 0x50000228
        ulp_edge_count1 = 0x5000022c
        ulp_alive_counter = 0x5000023c
        ulp_save_counter=0x50000244
        ulp_memory_pointer=0x50000248
        ulp_max_memory_pointer = 0x5000024c
        
        alive = hex(mem32[ulp_alive_counter])
        time.sleep(0.2)
        #print("Alive Counter")
        #print(hex(mem32[ulp_alive_counter]))


        # Ресет при липса на активност от ULP
        ulpReset = False

        if alive == hex(mem32[ulp_alive_counter]):
            print("ULP is not working") 
            counter.initCounter()
            db.write('532','0')
            db.write('533','0')
            time.sleep(1)

            ulpReset = True

        #Calculate the difference of the edge counter and handle overflow 
        currentEdge4 = counter.valFromMem(ulp_edge_count)
        currentEdge14 = counter.valFromMem(ulp_edge_count1)
        #print("Current Edge 4 = ",currentEdge4)
        #print("Current Edge 14 = ",currentEdge14)
        previousEdge4 = int(db.read('532'))
        previousEdge14 = int(db.read('533'))
        counter4 = int(db.read('437'))
        counter14 = int(db.read('439'))
        #print("Previous Edge 4 = ",previousEdge4)
        #print("Previous Edge 14 = ",previousEdge14)
        if ulpReset:
                print("ULP Reset exit!")
                
                currentEdge14 = previousEdge14
                currentEdge4 = previousEdge4
                return

        if currentEdge4 < previousEdge4:
            
            
            print("!!!Overflow 4 !!!")
            delta4 = (32767-previousEdge4) + currentEdge4
                #currentEdge4 = (32767-previousEdge4) + previousEdge4 + currentEdge4
                #print("New Current ", currentEdge4)
        else: 
            delta4 = currentEdge4-previousEdge4

        if currentEdge14 < previousEdge14:
            
            
            print("!!!Overflow 14 !!!")
            delta14 = (32767-previousEdge14) + currentEdge14
                #currentEdge4 = (32767-previousEdge4) + previousEdge4 + currentEdge4
                #print("New Current ", currentEdge4)
        else: 
            delta14 = currentEdge14-previousEdge14

        #print("Delta4 = ",delta4)
        #print("Delta14 = ",delta14)
        old4 = counter4
        old14 = counter14
        counter4 = counter4+delta4
        newEdgge4 = currentEdge4 + delta4
        db.write('437',counter4)
        db.write('532',currentEdge4)
        counter14 = counter14+delta14
        newEdgge14 = currentEdge14 + delta14
        db.write('439',counter14)
        db.write('533',currentEdge14)

        moment4 = counter4-old4
        moment14 = counter14 - old14
        #buffer.put('540',struct.pack("B", moment4) + b'\xff\xff')
       # 
        #buffer.put('541',struct.pack("B", moment14) + b'\xff\xff')
              
        buffer.put('540',moment4.to_bytes(2, 'big') )
        
        buffer.put('541',moment14.to_bytes(2, 'big'))
        
        return
     
    def initCounter():
        import esp32
        from machine import mem32
        from machine import Pin


        ulp_debounce_counter = 0x5000021c
        ulp_debounce_counter1 = 0x50000220
        ulp_debounce_max_count = 0x50000224
        ulp_edge_count = 0x50000228
        ulp_edge_count1 = 0x5000022c
        ulp_io_number = 0x50000234
        ulp_io_number2 = 0x50000238
        ulp_edge_count_to_wake_up = 0x50000230
        ulp_alive_counter = 0x5000023c
        ulp_save_period=0x50000240
        ulp_save_counter=0x50000244
        ulp_memory_pointer=0x50000248
        ulp_max_memory_pointer = 0x5000024c



        u = esp32.ULP()
        f = open('ulp_main.bin','rb')
        binary = f.read()
        # 5000 = 5ms. Импулс =  wakeUp_period*debounce*2

        u.set_wakeup_period(0, 13888)
        u.load_binary(0,binary)


        #IO 4
        mem32[ulp_io_number] = 10
        #IO 14
        mem32[ulp_io_number2] = 16
        #Колко edges с едно и също ниво са хванати
        mem32[ulp_debounce_counter] = 5
        mem32[ulp_debounce_counter1] = 5
        #Колко пъти трябва да има една и съща стойност, за да се приеме импулст

        mem32[ulp_debounce_max_count] = 2

        #Брой импулси - edge Counter/2

        mem32[ulp_edge_count] = 0
        mem32[ulp_edge_count1] = 0

        #При колко импулса ще ни събуди
        mem32[ulp_edge_count_to_wake_up] = 10

        #колко пъти се е будило, дали работи ULP-to (5ms )
        mem32[ulp_alive_counter] = 0
        #На колко будения да запазим стойност. 12000 -> минута. Макс -> 65000
        #wakeup * Save
        #mem32[ulp_save_period] = 60000
        period = db.read('421')
        #square(900/5000)
        #square(желано време/5000)
        #честота на запис = pow(savePeriod*ulpTime (5000))
        mem32[ulp_save_period] =  72*int(period)#6000
        #Не пипаме
        mem32[ulp_memory_pointer] = 0x10
        mem32[ulp_max_memory_pointer] = 0x168


        u.run(0)
        
        timestamp = device.getTimestamp() 


        #db.write('443',timestamp)
        #timestamp = device.setTimestamp()
        #db.write('443',timestamp)
        buffer.create('540')
        buffer.create('541')
class device(object):

    def restart():        
        machine.reset()
        
    
    def factoryReset():
        db.initDefaults()
        #db.store()

        machine.reset()
    def freeMemory():
        import gc
        return round(gc.mem_free()/1024)
    
    def serialNumber():
        import ubinascii
        
        return ubinascii.hexlify(machine.unique_id()).decode()
    
    def memoryTotal():
        import gc
        return round(gc.mem_alloc()/1024)

    
    def getTimestamp():
        #from machine import RTC
        
        #clock = RTC()
        #timeArray = clock.datetime()
        timestamp = time.time()+946684800
        if timestamp < 1664000000:
        #if timeArray[0] == 2000 :
            print("Wrong date")
            #if modem.isOn() == False:
            modem.turnOn()
            modem.registerNetwork()
            #modem.turnOn()
            higpsTimestamp = modem.getTimeF()
            
            if len(higpsTimestamp) == 10: 
                ttt=time.localtime(int(higpsTimestamp)-946684800)
                machine.RTC().init((ttt[0],ttt[1],ttt[2],0,ttt[3],ttt[4],ttt[5],0))
                print(machine.RTC().datetime())
                timestamp = time.time()+946684800
            else: 
                print("Cannot get time")
        else :
            print("Date OK")
        
        return timestamp

    def setTimestamp(timestamp = False):
        if timestamp:
            higpsTimestamp = timestamp
        else:
            modem.turnOn()
            higpsTimestamp = modem.getTimeF()
            
        if len(higpsTimestamp) == 10: 
            ttt=time.localtime(int(higpsTimestamp)-946684800)
            machine.RTC().init((ttt[0],ttt[1],ttt[2],0,ttt[3],ttt[4],ttt[5],0))
            print(machine.RTC().datetime())
            timestamp = time.time()+946684800



class fw(object):
    def __init__(self):
        print("Core v. 1")
        self.gps = GPS()
        self.gps.turn_on_gps()
       
        #if  machine.wake_reason() != 0 :
        #    machine.reset()
        global db
        global modem
        global protocol
        global Gimei
        machine.freq(80000000)
        Gimei =  db.read('200')
        if Gimei == False:
            modem.turnOn()
            imei = modem.getImei()
            protocol.imei = imei
            modem.registerNetwork()
            db.initDefaults()

            db.store()
            gc.collect()
            print(gc.mem_free())
            db = database()
            Gimei = db.read('200').decode('utf-8')

            protocol.main('defaults')
        else: 
            Gimei = Gimei.decode('utf-8')


    def antenna_report(self,antenna_for_report):
        try:
            self.measure()
        
        except Exception as e:
            print("")
           #setError("Error in measure" + (str(e)))
        
        
        if len(antenna_for_report) > 0:
            for antenna, data in antenna_for_report.items():
                print(f"Антена: {antenna}, Прочетена пъти: {data['count']}")
                        
                print("Writing 657:", antenna[:24])
                print("Writing 257:", antenna_for_report[antenna]['data']['timestamp_gps'])
                print("Writing 254:", antenna_for_report[antenna]['data']['latitude'])
                print("Writing 255:", antenna_for_report[antenna]['data']['longitude'])
                print("Writing 519:", antenna_for_report[antenna]['data']['num_satellites'])
                print("Writing 256:", antenna_for_report[antenna]['data']['altitude'])
                print("Writing 258:", antenna_for_report[antenna]['data']['ground_speed'])
                            
                            
                            
                db.write('657', antenna[:24])
                db.write('257', str(antenna_for_report[antenna]['data']['timestamp_gps']) or "0")  
                db.write('254', str(antenna_for_report[antenna]['data']['latitude']) or "0")  
                db.write('255', str(antenna_for_report[antenna]['data']['longitude']) or "0")  
                db.write('519', str(antenna_for_report[antenna]['data']['num_satellites']) or "0") 
                db.write('256', str(antenna_for_report[antenna]['data']['altitude']) or "0")
                db.write('258', str(antenna_for_report[antenna]['data']['ground_speed']) or "0")
                            
                            
                time.sleep(0.1)

                        
                try:
                    self.report(True)
                    del antenna_for_report[antenna]
                                
                except Exception as e:
                    setError("Error in report" + (str(e)))                
                            
        else:
                print("NO RFID found")    
        
    
    def start(self):
       
        global firmwareVersion
        global timeOffset
        global gpsReport
        global registrationTime
        print("Firmware v. ", firmwareVersion)
        
        global connectionSuccess
        
                      
        self.antenna = Antenna()       # Инициализация на Antenna инстанция
        self.this_antenna = None        # Променлива за текущата антена
        
        global latitude
        global longitude
        global num_satellites
        global altitude
        global ground_speed
        global timestamp_gps

        
        
        f = 0
        #while int(db.read('290')) > 6000 or f == 0 : 
        
        tttime = int(time.time())
        _thread.start_new_thread(self.antenna.process_packets, ())
        while True:
            try:
                self.measure()        
            except Exception as e:
                print("")
                #setError("Error in measure" + (str(e)))
            
            self.gps.read_gps_data()
           
            
            
            
            wdt = machine.WDT(timeout=5000000)
            wdt.feed()
            
            
            
            report_time = int(time.time()) - tttime
            times = int(db.read('421'))
            if report_time > times:
                if len(self.antenna.antenna_count) != 0:
                    antenna_for_report = self.antenna.antenna_count.copy()
                    self.antenna_report(antenna_for_report)
                    self.antenna.antenna_count.clear()
                    print("ok2")
                else:
                    try:
                                     
                        db.write('657', "0")
                        db.write('257', str(timestamp_gps) or "0")  
                        db.write('254', str(latitude) or "0")  
                        db.write('255', str(longitude) or "0")  
                        db.write('519', str(num_satellites) or "0") 
                        db.write('256', str(altitude) or "0")
                        db.write('258', str(ground_speed) or "0")

                        self.report(True)
                        
                        
                    except Exception as e:
                        
                        setError("Error in report" + (str(e)))
                        
                tttime = int(time.time())
                
            
            
        

    
                
               
    
        
        

    def report(self,alarm):
        
        modem.uart = machine.UART(1, modem.br, rx=modem.rx, tx=modem.tx, txbuf=1024, rxbuf=2048)
        time.sleep(0.1)
        
        #counter.getSamplings()
        global connectionSuccess
        try: 
            if modem.isOn() == False:
                turnOncounter =0 
                while modem.isOn() == False and turnOncounter < 30: 
                    
                    modemOn = modem.turnOn()
                    time.sleep(0.5)
            
                #time.sleep(2)
            buffer.get('540')
            buffer.get('541')
            print("Reporting")
            

            self.getGSMInfo()

            if alarm:
                protocol.main('samplingsAlarm')        
            else : 
                protocol.main('samplings')
                

        except Exception as e:
            print("")
            setError(" Error in report "+(str(e)))
            protocol.main('dataBat')
        print("Connection success", connectionSuccess)
        if connectionSuccess: 
            db.write('440',0)
            buffer.remove('540')
            buffer.remove('541')
            buffer.create('540')
            buffer.create('541')
            db.write('522','0')
            db.store()

    def getGSMInfo(self):
        data = modem.getCPSI()
        #Cat M1 'LTE;CAT-M1,Online,284-05,0x0066,280577,136,EUTRAN-BAND3,1550,5,5,-12,-108,-82,10OK'
        #2G 'GSM,Online,284-05,0x0737,10961,987;EGSM;900,-75,0,37-37OK'
        #NB-IoT 'LTE;NB-IOT,Online,284-01,0x00C7,8166603,284,EUTRAN-BAND8,3687,0,0,-10,-83,-73,13OK'
        network = modem.getCPSI()
        #'LTE;NB-IOT,Online,284-01,0x00C7,8282059,323,EUTRAN-BAND8,3687,0,0,-10,-99,-89,20OK'
        #['LTE;CAT-M1', 'Online', '284-05', '0x0066', '280577', '136', 'EUTRAN-BAND3', '1550', '5', '5', '-12', '-108', '-82', '10OK']
        #['LTE;NB-IOT', 'Online', '284-01', '0x00C7', '8166603', '284', 'EUTRAN-BAND8', '3687', '0', '0', '-10', '-83', '-73', '13OK']
        

        try: 
            networkParams = network.split(',')
            if "LTE" in networkParams[0]:
                networkType = networkParams[0].split(';')
                db.write('230',networkType[1])  #Network Bearer 
                db.write('231',networkParams[12]) #Radio Signal Strength
                db.write('232',networkParams[11]) #Link Quality
                db.write('234',networkParams[4]) #Cell ID
                mcc = networkParams[2].split('-')

                db.write('235',mcc[1]) #SMNC
                db.write('236',mcc[0]) #SMCC
                db.write('237',networkParams[13][:-2]) #SignalSNR
                db.write('238',networkParams[3]) #LAC
            elif 'GSM' in networkParams[0]: 
                db.write('230',networkParams[0]) #Network Bearer 
                db.write('231',networkParams[6]) #Radio Signal Strength
                db.write('232',networkParams[8][0:2]) #Link Quality
                db.write('234',networkParams[4]) #Cell ID
                mcc = networkParams[2].split('-')

                db.write('235',mcc[1]) #SMNC
                db.write('236',mcc[0]) #SMCC
                db.write('237',networkParams[8][2:-2]) #SignalSNR
                db.write('238',networkParams[3]) #LAC
                
        except Exception as e:
            print("Exception !!! ")
            print(e) 

    def prepareSleep(self,t):
        
        print("GOING TO SLEEP FOR ")
        print(t)
        t = t+1
        #GSM pwr
        #PWR Key
        
        modem.turnOff()
        
        #machine.Pin(PmodemPWRKey, machine.Pin.IN,machine.Pin.PULL_UP)
        machine.Pin(PmodemTx, machine.Pin.IN)
        machine.Pin(PmodemRx, machine.Pin.IN)
        machine.Pin(PmodemDTR, machine.Pin.IN)
        machine.Pin(Pscl, machine.Pin.IN)
        machine.Pin(Psda, machine.Pin.IN)
        machine.Pin(PperipherialPower, machine.Pin.IN)
        machine.Pin(PmodemPower, machine.Pin.IN)
        machine.Pin(Pbuzzer, machine.Pin.IN)
        #machine.Pin(Pinput14, machine.Pin.IN)
        #machine.Pin(Pinput4, machine.Pin.IN)
        #machine.Pin(Preed, machine.Pin.IN)

        #machine.Pin(PmodemPWRKey, machine.Pin.IN,machine.Pin.PULL_DOWN)
        #machine.Pin(PmodemPWRKey, machine.Pin.IN,machine.Pin.PULL_DOWN)


        #led.value(0)
        
        st = self.goodNight(t*1000)


    def goodNight(self,timeS):
        

        try:
            db.store()
            print("Going to Deep Sleep")
            machine.deepsleep(timeS)
        except: 
            machine.reset()
    def measure(self):
       
        #print_antenna_counts()
        
        adc = machine.Pin(PperipherialPower,machine.Pin.OUT)
            
            
        machine.Pin(PperipherialPower,machine.Pin.OUT).value(1)
            #time.sleep(5)

        externalPower = round(self.adcMeasure(b'\xd0')*11.5,2)
        #db.write('290',str(round(externalPower),2))
        print("External Power",externalPower)
        machine.Pin(PperipherialPower,machine.Pin.OUT).value(0)
        
        if externalPower < 9000:
            print("low voltage")
            sleep_time = int(db.read('422'))
            self.prepareSleep(sleep_time)
        
        
    def adcMeasure(self,n):
        i2c = machine.SoftI2C(freq=100000,scl=machine.Pin(Pscl),sda=machine.Pin(Psda))
        i2c.start()
        #print(i2c.scan())
        i2c.writeto(104,b'\x18')
        time.sleep(0.01)
        i2c.writeto(104,n)
        time.sleep(0.01)
        sampling =int.from_bytes(i2c.readfrom(104,4)[0:2],"big")
        
        return sampling

def setError(error):
        global errors
        global errorsSent
        errors += " "+ error 
        errorsSent = False   
        print(error)
db = database()
modem = sim7070()
protocol = findyIoT()




