import requests

try:
    while True:
        url = 'http://127.0.0.1:8000/get_request'

        x = requests.get(url)

        #print the response text (the content of the requested file):

        print(x.text)
        
except KeyboardInterrupt:
    # Ctrl+C'ye basılırsa programı kapat
    pass
