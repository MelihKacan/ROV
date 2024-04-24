import requests

try:
    rotary_value = 0
    joyistik_value = 0
    while True:            
        joyistik_value += 1
        
        rotary_value += 1
                
        url = 'http://127.0.0.1:8000/post_request'
        myobj = {'joyistik': joyistik_value,'rotary': rotary_value}

        x = requests.post(url, json = myobj)

        #print the response text (the content of the requested file):

        print(x.text)
        
except KeyboardInterrupt:
    # Ctrl+C'ye basılırsa programı kapat
    pass
