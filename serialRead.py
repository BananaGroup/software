import serial, sys, time, json, os, requests

class serialRead:

    def __init__(self):
        self.serialPort = '/dev/tty.usbmodemfa131'
        self.logFileLocation = 'output.log'
        self.apiUrl = 'http://files.joshwalwyn.com/university/307CR/hotwire/server/run.php'
        if '--batch' in sys.argv:
            self.sendLog()
            sys.exit()
        self.checkSerial()
        self.openSerial()
        self.serialBuffer = []
        if not self.apiAvailable():
            self.prepareLog()
        if '--forceHeat' in sys.argv:
            self.heatOn()

    def heatOn(self):
        self.ser.write(b'1')
        print 'heating'

    def buffer(self):
        if len(self.serialBuffer) == 0:
            for reading in self.jsonIn['readings']:
                self.serialBuffer.append([])
        else:
            i = 0
            for reading in self.jsonIn['readings']:
                self.serialBuffer[i].append(reading['value'])
                i+=1
        if len(self.serialBuffer[0]) == 1000:
            i = 0
            for reading in self.jsonIn['readings']:
                reading['value'] = sum(self.serialBuffer[i]) / len(self.serialBuffer[i])
                i+=1
            self.serialBuffer = []
            self.handle()


    def openSerial(self):
        self.ser = serial.Serial()
        self.ser.port = self.serialPort
        self.ser.baudrate = 9600
        self.ser.open()

    def sendLog(self):
        print 'processing batch'
        payload = {'file': open(self.logFileLocation, 'rb')}
        r = requests.post('%s?datatype=csv' % self.apiUrl, files=payload)
        print r.text

    def checkSerial(self):
        if not os.path.exists(self.serialPort):
            print 'port unavailable'
            sys.exit()

    def readSerial(self):
        self.checkSerial()
        self.jsonIn = json.loads(self.ser.readline())
        if(self.jsonIn['timestamp'] == False):
            self.jsonIn['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.buffer()

    def handle(self):
        if self.apiAvailable():
            self.apiCall()
        else:
            self.writeToLog()
        self.printOut()

    def prepareLog(self):
        with open(self.logFileLocation, 'w') as f:
            fields = '"user_id","sensor_id","value","timestamp"\n'
            f.write(fields)
            f.flush

    def writeToLog(self):
        with open(self.logFileLocation, 'a+') as f:
            for reading in self.jsonIn['readings']:
                data = '%s,%s,%s,%s\n' % (self.jsonIn['user_id'], reading['sensor_id'], reading['value'], self.jsonIn['timestamp'])
                f.write(data)
                f.flush()

    def apiCall(self):
        for reading in self.jsonIn['readings']:
            payload = {'user_id': self.jsonIn['user_id'], 'sensor_id': reading['sensor_id'], 'value': reading['value'], 'timestamp': self.jsonIn['timestamp']}
            r = requests.post(self.apiUrl, data=payload)
            print r.text

    def printOut(self):
        print 'user_id:', self.jsonIn['user_id']
        print 'head:', self.jsonIn['readings'][0]['value']
        print 'core:', self.jsonIn['readings'][1]['value']
        print 'outside:', self.jsonIn['readings'][2]['value']
        print 'time:', self.jsonIn['timestamp']
        print '-----------'

    def apiAvailable(self):
        return False


sr = serialRead()

while True:
    sr.readSerial()