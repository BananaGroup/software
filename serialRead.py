import serial, sys, time, json, datetime

ser = serial.Serial('/dev/tty.usbmodemfa131', 9600)

with open('output.log', 'a+') as f:
    while True:
        jsonIn = json.loads(ser.readline())
        if(jsonIn['timestamp'] == False):
            jsonIn['timestamp'] = datetime.datetime.utcnow()
        
        print 'head:', jsonIn['readings'][0]['value']
        print 'core:', jsonIn['readings'][1]['value']
        print 'outside:', jsonIn['readings'][2]['value']
        print 'time:', jsonIn['timestamp']
        print '-----------'

        #f.write(ser.readline())
        #f.flush()
        #time.sleep(10)