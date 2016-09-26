
# -*- coding: utf-8 -*-

import serial
import time



ser = serial.Serial('/dev/ttyACM0', 9600)

varl = 'temp'


def tempupdate() :
        var1 = ser.readline()
        varl.replace("\r\n","")
        fob = open('/var/www/html/index.html', 'w')
        fob.write("""   <html>
                        <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="refresh" content="5">
                        <link rel="stylesheet" type="text/css" href="mystyles.css" />
			</head>
			<body>
			<div>""" +
			'<h1>downstairs temperature:</h1> ' +
			'<h2>'+ var1 + "°" + 'C' + '</h2>' + 
			'<h3>' + time.strftime('%l:%M%p on %b %d, %Y') + '</h3>'+
			'</div>'+
			'</body>'+
			'</html>'
			)
        fob.close()

while 1:
        tempupdate()





