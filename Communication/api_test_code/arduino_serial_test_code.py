import serial
import requests

# Arduino'nun bağlı olduğu seri portunu belirtin
serial_port = 'COM3'  # Arduino'nun bağlı olduğu port

# Seri portu ve hızı (baud rate) ayarlayın
ser = serial.Serial(serial_port, 9600)  # Arduino kodunda belirttiğiniz baud rate ile eşleşmeli

try:
    while True:
        # Seri porttan bir satır okuyun
        line = ser.readline().decode().strip()
            
                
        url = 'http://127.0.0.1:8000/post_request'
        myobj = {'joyistik': line,'rotary':123}

        x = requests.post(url, json = myobj)

        #print the response text (the content of the requested file):

        print(x.text)
        
except KeyboardInterrupt:
    # Ctrl+C'ye basılırsa programı kapat
    ser.close()
