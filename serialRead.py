import serial, sys, time, json, os

class serialRead:

    def __init__(self):
        self.serialPort = '/dev/tty.usbmodemfd121'
        self.logFileLocation = 'output.log'
        if '--batch' in sys.argv:
            self.sendLog()
            sys.exit()
        self.checkSerial()
        self.openSerial()

    def openSerial(self):
        self.ser = serial.Serial()
        self.ser.port = self.serialPort
        self.ser.baudrate = 9600
        self.ser.open()

    def sendLog(self):
        print 'processing batch'
        # send to api
        print 'done'

    def checkSerial(self):
        if not os.path.exists(self.serialPort):
            print 'port unavailable'
            sys.exit()

    def readSerial(self):
        self.checkSerial()
        self.jsonIn = json.loads(self.ser.readline())
        if(self.jsonIn['timestamp'] == False):
            self.jsonIn['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

    def prepareLog(self):
        with open(self.logFileLocation, 'w') as f:
            fields = '"s01","s02","s03","timestamp"\n'
            f.write(fields)
            f.flush

    def writeToLog(self):
        with open(self.logFileLocation, 'a+') as f:
            data = '%s,%s,%s,%s\n' % (self.jsonIn['readings'][0]['value'], self.jsonIn['readings'][1]['value'], self.jsonIn['readings'][2]['value'], self.jsonIn['timestamp'])
            f.write(data)
            f.flush()

    def apiCall(self):
        data = '?s01=%s&s02=%s&s03=%s&timestamp=%s' % (self.jsonIn['readings'][0]['value'], self.jsonIn['readings'][1]['value'], self.jsonIn['readings'][2]['value'], self.jsonIn['timestamp'])
        print data

    def printOut(self):
        print 'head:', self.jsonIn['readings'][0]['value']
        print 'core:', self.jsonIn['readings'][1]['value']
        print 'outside:', self.jsonIn['readings'][2]['value']
        print 'time:', self.jsonIn['timestamp']
        print '-----------'

    def apiAvailable(self):
        return False


sr = serialRead()

if not sr.apiAvailable():
    sr.prepareLog()
    while True:
        sr.readSerial()
        sr.writeToLog()

if sr.apiAvailable():
    while True:
        sr.readSerial()
        sr.apiCall()