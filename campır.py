#!/usr/bin/python

import RPi.GPIO as GPIO

import time

import smtplib

from email.MIMEMultipart import MIMEMultipart

from email.MIMEImage import MIMEImage

from email.MIMEText import MIMEText

from email.Utils import COMMASPACE, formatdate

from email import Encoders

import subproces

#KAMERA KAYDI VE MAİL YOLLAMA####
def sendEmail():
    grab_cam = subprocess.Popen(“sudo fswebcam - p YUYV image1.jpeg”, shell = True)
    grab_cam.wait()
    image_path = ‘image1.jpeg’
    username = “cemakdemir99 @ gmail.com”  # gönderilen mail hesabın adını yazıyoruz
    password = “#######”  # gönderilen mail hesabın şifresini yazıyoruz
    COMMASPACE = ‘, ’
    message = MIMEMultipart()
    message[‘Subject’] = ‘Hareket Algilandi’
    me = ‘####### @ gmail.com’  # gönderilecek mail hesabın adını yazıyoruz
    receivers = ‘########@ gmail.com’  # gönderilecek mail hesabın adını yazıyoruz
    message[‘From’] = me
    message[‘To’] = COMMASPACE.join(receivers)
    message.preamble = ‘Hareket’
    fp = open(‘image1.jpeg’, ‘rb’)
    img = MIMEImage(fp.read())
    fp.close()
    message.attach(img)
    try:
        server = smtplib.SMTP(“smtp.gmail.com”, 587)  # portu mail servis saglayacisi
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(me, receivers.split(“, ”), message.as_string())
        server.close()
        print ‘mail gonderildi’

    except:
        print “mail gonderilemedi”


#PIR SENSÖR KODLARI###

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

try:

    print “PIR Modul Testi(Cikmak icin CTRL + C’ye basin )”
    time.sleep(2)
    print “Hazir”

while True:

    if GPIO.input(PIR_PIN):
        print “Hareket Algilandi!”
        sendEmail()
        time.sleep(1)

except KeyboardInterrupt:
    print “Cikis”
    GPIO.cleanup()
