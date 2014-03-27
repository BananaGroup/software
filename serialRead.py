import serial, sys, time, json, os, requests

class serialRead:

    def __init__(self):
        self.serialPort = '/dev/tty.usbmodemfd121'
        self.logFileLocation = 'output.log'
        self.apiUrl = 'http://projects.jjw.al/hotwire/service/'
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
        payload = {'file': open(self.logFileLocation, 'rb')}
        r.requests.post('%s?datatype=csv' % self.apiUrl, files=logFile)
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
            fields = '"user_id","sensor_id","value","timestamp"\n'
            f.write(fields)
            f.flush

    def writeToLog(self):
        with open(self.logFileLocation, 'a+') as f:
            for reading in self.jsonIn['readings']:
                data = '%s,%s,%s,%s\n' % (self.jsonIn['userId'], reading['sensorId'], reading['value'], self.jsonIn['timestamp'])
                f.write(data)
                f.flush()

    def apiCall(self):
        for reading in self.jsonIn['readings']:
            payload = {'user_id': self.jsonIn['user_id'], 'sensor_id': reading['sensor_id'], 'value': reading['value'], 'timestamp': self.jsonIn['timestamp']}
            r.requests.post(self.apiUrl, params=payload)

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