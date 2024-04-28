import cv2
import numpy as np
import pandas as pd
import screeninfo
import serial
import time

# Ekran bilgileri
screen = screeninfo.get_monitors()[0]
screen_width = screen.width
screen_height = screen.height


ser = serial.Serial('COM3',9600)
time.sleep(2)

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('C:\\Files_Desktop\\Python\\Django\\CakaRov\\Communication\\api\\colors.csv', names=index, header=None)

def getColorName(R, G, B):

    minimum = 1000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            color_name = csv.loc[i, "hex"]
    return color_name

def mission(mission_color):
    veri = 0

    cap = cv2.VideoCapture(0)
    # Kamera, Webcam kullanırken ters gözükmektedir ancak ROV aracında düz şekilde olacaktır. Değiştirilmemesi gerekmektedir.

    while True:
    # Kamera yakalamak 
        _, frame = cap.read()

        frame = cv2.resize(frame,(screen_width,screen_height))

        # Renkleri HSV renk uzayına dönüştürüyoruz
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Yeşil rengin HSV'deki değer aralığı
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        #Mavi rengin HSV'deki değer aralığı
        lower_blue = np.array([80, 100, 100])
        upper_blue = np.array([140, 255, 255])

        # Kırmızı rengin HSV'deki değer aralığı
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Maskeleme işlemi uyguluyoruz
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        #Yeşil rengi maskeliyoruz
        res_green = cv2.bitwise_and(frame, frame, mask=mask_green)

        #Mavi rengi maskeliyoruz
        res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)

        # Kırmızı rengi maskeliyoruz
        res_red = cv2.bitwise_and(frame, frame, mask=mask_red2)

        cx = int(frame.shape[1] / 2)
        cy = int(frame.shape[0] / 2)

        color_name = getColorName(frame[cy, cx][2], frame[cy, cx][1], frame[cy, cx][0]) + ' R=' + str(frame[cy, cx][2]) + ' G=' + str(frame[cy, cx][1]) + ' B=' + str(frame[cy, cx][0])
        
        #Ekranı ortalayacak şekilde merkez noktamızı oluşturuyoruz
        #cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        print(color_name)
        

        # Merkez noktadaki renk değerini alıyoruz
        merkez_renk = frame[cy, cx]
        
        merkez_renk_RGB = (merkez_renk[2], merkez_renk[1], merkez_renk[0])
        
        # Belirlediğimiz yeşil tonunun aralığını ayarlıyoruz
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        if mission_color == "green":
            # Merkez noktadaki rengin istediğimiz renk olup olmadığını kontrol ediyoruz
            if np.all(merkez_renk_RGB >= lower_green) and np.all(merkez_renk_RGB <= upper_green):
                print("YESIL")
                """ser.write(b'G')"""
            else:
                print("Merkez nokta, istenilen YESIL tonu içinde değil."),
                print(merkez_renk_RGB)

        elif mission_color == "red":
            if np.all(merkez_renk_RGB >= lower_red1) and np.all(merkez_renk_RGB <= upper_red1):
                print("KIRMIZI")
                """ser.write(b'G')"""
            elif np.all(merkez_renk_RGB >= lower_red2) and np.all(merkez_renk_RGB <= upper_red2):
                print("KIRMIZI")
                """ser.write(b'G')"""
            else:
                print("Merkez nokta, istenilen KIRMIZI tonu içinde değil."),
                print(merkez_renk_RGB)
                
        elif mission_color == "blue":
            if np.all(merkez_renk_RGB >= lower_blue) and np.all(merkez_renk_RGB <= upper_blue):
                print("MAVI")
                """ser.write(b'G')"""
            else:
                print("Merkez nokta, istenilen MAVI tonu içinde değil."),
                print(merkez_renk_RGB)

        """# Ekranda yeşil renk var mı kontrol ediyoruz 
        if np.sum(res_green) > 0:
            print("Yeşil renk bulundu!")

        #Ekranda mavi renk var mı kontrol ediyoruz 
        if np.sum(res_blue) > 0:
            print("Mavi renk bulundu!")

        # Ekranda kırmızı renk var mı kontrol ediyoruz 
        if np.sum(res_red) > 0:
            print("Kırmızı renk bulundu!")"""

        if mission_color == "green":
            if np.sum(res_green) > 0:
                # Yeşil rengin bulunduğu piksellerin koordinatlarını alıyoruz
                green_pixels = np.argwhere(res_green > 0)

                # Yeşil rengin bulunduğu ilk pikselin koordinatlarını alıyoruz
                green_pixel = green_pixels[0]

                # Yeşil rengin bulunduğu pikselin koordinatlarını yazdırıyoruz
                print("Yeşil renk, x =", green_pixel[1], ", y =", green_pixel[0], " konumunda bulundu.")
                #ser.write(b'yesil :  x = {}, y = {}'.format(green_pixel[1],green_pixel[0]))
                    # YEŞİL RENK 
                if green_pixel[1] >= 0 and green_pixel[1] <= 480 and green_pixel[0] >= 0 and green_pixel[0] <= 270 :
                    veri = 1
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif green_pixel[1] >= 0 and green_pixel[1] <= 480 and green_pixel[0] >= 271 and green_pixel[0] <= 540 :
                    veri = 2
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 0 and green_pixel[1] <= 480 and green_pixel[0] >= 541 and green_pixel[0] <= 810 :
                    veri = 3
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 0 and green_pixel[1] <= 480 and green_pixel[0] >= 811 and green_pixel[0] <= 1080 :
                    veri = 4
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 







                elif green_pixel[1] >= 481 and green_pixel[1] <= 960 and green_pixel[0] >= 0 and green_pixel[0] <= 270 :
                    veri = 5
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif green_pixel[1] >= 481 and green_pixel[1] <= 960 and green_pixel[0] >= 271 and green_pixel[0] <= 540 :
                    veri = 6
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 481 and green_pixel[1] <= 960 and green_pixel[0] >= 541 and green_pixel[0] <= 810 :
                    veri = 7
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 481 and green_pixel[1] <= 960 and green_pixel[0] >= 811 and green_pixel[0] <= 1080 :
                    veri = 8
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 





                elif green_pixel[1] >= 961 and green_pixel[1] <= 1440 and green_pixel[0] >= 0 and green_pixel[0] <= 270 :
                    veri = 9
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif green_pixel[1] >= 961 and green_pixel[1] <= 1440 and green_pixel[0] >= 271 and green_pixel[0] <= 540 :
                    veri = 10
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 961 and green_pixel[1] <= 1440 and green_pixel[0] >= 541 and green_pixel[0] <= 810 :
                    veri = 11
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 961 and green_pixel[1] <= 1440 and green_pixel[0] >= 811 and green_pixel[0] <= 1080 :
                    veri = 12
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)





                
                elif green_pixel[1] >= 1441 and green_pixel[1] <= 1920 and green_pixel[0] >= 0 and green_pixel[0] <= 270 :
                    veri = 13
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif green_pixel[1] >= 1441 and green_pixel[1] <= 1920 and green_pixel[0] >= 271 and green_pixel[0] <= 540 :
                    veri = 14
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 1441 and green_pixel[1] <= 1920 and green_pixel[0] >= 541 and green_pixel[0] <= 810 :
                    veri = 15
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif green_pixel[1] >= 1441 and green_pixel[1] <= 1920 and green_pixel[0] >= 811 and green_pixel[0] <= 1080 :
                    veri = 16
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)
        if mission_color == "red":
            if np.sum(res_red) > 0:
                # Kırmızı rengin bulunduğu piksellerin koordinatlarını alıyoruz
                red_pixels = np.argwhere(res_red > 0)

                # Kırmızı rengin bulunduğu ilk pikselin koordinatlarını alıyoruz
                red_pixel = red_pixels[0]

                # Kırmızı rengin bulunduğu pikselin koordinatlarını yazdırıyoruz
                print("Kırmızı renk, x =", red_pixel[1], ", y =", red_pixel[0], " konumunda bulundu.")
                #ser.write(b'Kirmizi :  x = {}, y = {}'.format(red_pixel[1],red_pixel[0]))
                
                # KIRMIZI RENK 



                if red_pixel[1] >= 0 and red_pixel[1] <= 480 and red_pixel[0] >= 0 and red_pixel[0] <= 270 :
                    veri = 1
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif red_pixel[1] >= 0 and red_pixel[1] <= 480 and red_pixel[0] >= 271 and red_pixel[0] <= 540 :
                    veri = 2
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 0 and red_pixel[1] <= 480 and red_pixel[0] >= 541 and red_pixel[0] <= 810 :
                    veri = 3
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 0 and red_pixel[1] <= 480 and red_pixel[0] >= 811 and red_pixel[0] <= 1080 :
                    veri = 4
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 







                elif red_pixel[1] >= 481 and red_pixel[1] <= 960 and red_pixel[0] >= 0 and red_pixel[0] <= 270 :
                    veri = 5
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif red_pixel[1] >= 481 and red_pixel[1] <= 960 and red_pixel[0] >= 271 and red_pixel[0] <= 540 :
                    veri = 6
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 481 and red_pixel[1] <= 960 and red_pixel[0] >= 541 and red_pixel[0] <= 810 :
                    veri = 7
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 481 and red_pixel[1] <= 960 and red_pixel[0] >= 811 and red_pixel[0] <= 1080 :
                    veri = 8
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 





                elif red_pixel[1] >= 961 and red_pixel[1] <= 1440 and red_pixel[0] >= 0 and red_pixel[0] <= 270 :
                    veri = 9
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif red_pixel[1] >= 961 and red_pixel[1] <= 1440 and red_pixel[0] >= 271 and red_pixel[0] <= 540 :
                    veri = 10
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 961 and red_pixel[1] <= 1440 and red_pixel[0] >= 541 and red_pixel[0] <= 810 :
                    veri = 11
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 961 and red_pixel[1] <= 1440 and red_pixel[0] >= 811 and red_pixel[0] <= 1080 :
                    veri = 12
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)





                
                elif red_pixel[1] >= 1441 and red_pixel[1] <= 1920 and red_pixel[0] >= 0 and red_pixel[0] <= 270 :
                    veri = 13
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif red_pixel[1] >= 1441 and red_pixel[1] <= 1920 and red_pixel[0] >= 271 and red_pixel[0] <= 540 :
                    veri = 14
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 1441 and red_pixel[1] <= 1920 and red_pixel[0] >= 541 and red_pixel[0] <= 810 :
                    veri = 15
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif red_pixel[1] >= 1441 and red_pixel[1] <= 1920 and red_pixel[0] >= 811 and red_pixel[0] <= 1080 :
                    veri = 16
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)
                
                
        if mission_color == "blue":
            if np.sum(res_blue) > 0:
                # Mavi rengin bulunduğu piksellerin koordinatlarını alıyoruz
                blue_pixels = np.argwhere(res_blue > 0)

                # Mavi rengin bulunduğu ilk pikselin koordinatlarını alıyoruz            
                blue_pixel = blue_pixels[0]

                # Mavi rengin bulunduğu pikselin koordinatlarını yazdırıyoruz
                print("Mavi renk, x =", blue_pixel[1], ", y =", blue_pixel[0], " konumunda bulundu.")
                #ser.write(b'Mavi : x = {}, y = {}'.format(blue_pixel[1],blue_pixel[0]))


            
                if blue_pixel[1] >= 0 and blue_pixel[1] <= 480 and blue_pixel[0] >= 0 and blue_pixel[0] <= 270 :
                    veri = 1
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif blue_pixel[1] >= 0 and blue_pixel[1] <= 480 and blue_pixel[0] >= 271 and blue_pixel[0] <= 540 :
                    veri = 2
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 0 and blue_pixel[1] <= 480 and blue_pixel[0] >= 541 and blue_pixel[0] <= 810 :
                    veri = 3
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 0 and blue_pixel[1] <= 480 and blue_pixel[0] >= 811 and blue_pixel[0] <= 1080 :
                    veri = 4
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 







                elif blue_pixel[1] >= 481 and blue_pixel[1] <= 960 and blue_pixel[0] >= 0 and blue_pixel[0] <= 270 :
                    veri = 5
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif blue_pixel[1] >= 481 and blue_pixel[1] <= 960 and blue_pixel[0] >= 271 and blue_pixel[0] <= 540 :
                    veri = 6
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 481 and blue_pixel[1] <= 960 and blue_pixel[0] >= 541 and blue_pixel[0] <= 810 :
                    veri = 7
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 481 and blue_pixel[1] <= 960 and blue_pixel[0] >= 811 and blue_pixel[0] <= 1080 :
                    veri = 8
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 





                elif blue_pixel[1] >= 961 and blue_pixel[1] <= 1440 and blue_pixel[0] >= 0 and blue_pixel[0] <= 270 :
                    veri = 9
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif blue_pixel[1] >= 961 and blue_pixel[1] <= 1440 and blue_pixel[0] >= 271 and blue_pixel[0] <= 540 :
                    veri = 10
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 961 and blue_pixel[1] <= 1440 and blue_pixel[0] >= 541 and blue_pixel[0] <= 810 :
                    veri = 11
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 961 and blue_pixel[1] <= 1440 and blue_pixel[0] >= 811 and blue_pixel[0] <= 1080 :
                    veri = 12
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)





                
                elif blue_pixel[1] >= 1441 and blue_pixel[1] <= 1920 and blue_pixel[0] >= 0 and blue_pixel[0] <= 270 :
                    veri = 13
                    ser.write(str(veri).encode())

                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)

                elif blue_pixel[1] >= 1441 and blue_pixel[1] <= 1920 and blue_pixel[0] >= 271 and blue_pixel[0] <= 540 :
                    veri = 14
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 1441 and blue_pixel[1] <= 1920 and blue_pixel[0] >= 541 and blue_pixel[0] <= 810 :
                    veri = 15
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap) 

                elif blue_pixel[1] >= 1441 and blue_pixel[1] <= 1920 and blue_pixel[0] >= 811 and blue_pixel[0] <= 1080 :
                    veri = 16
                    ser.write(str(veri).encode())
                    
                    # Cevabı al ve yazdır
                    cevap = ser.readline().decode()
                    print("Alınan cevap:", cevap)
                



    





    



        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')