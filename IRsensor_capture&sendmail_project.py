#Wireless project
#From ductam.astro with love

import RPi.GPIO as GPIO

from time import sleep
import time
from picamera import PiCamera#, Color

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR

#Get date, time from datetime.now() and convert to string
filename = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())

#Setting Camera
camera = PiCamera()
camera.resolution = 'HD'
#camera.resolution = (2592, 1944)
#The minimum resolution is 64×64, max is 2592*1944.
camera.framerate = 15
camera.brightness = 60

SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'ductam.astro@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'hsxpkekkikunxkgt'  #change this to match your gmail password
GMAIL_RECEIVE = '15520755@gm.uit.edu.vn'

def send_mail():
    mail_content = "Hello, Ductam! " + "\n\r WARNING!!!  Someone was detected at " + time.ctime() + '''
    The mail is sent using Python SMTP library.
    From Raspberry, Thanks'''
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = GMAIL_RECEIVE
    message['Subject'] = 'Canh bao!! Vat the la xuat hien' 
    camera.capture('/home/pi/Desktop/%s.jpg' % filename)
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = ('/home/pi/Desktop/%s.jpg' % filename)
    img_data = open(attach_file_name, 'rb').read() 
    payload = MIMEImage(img_data, filename=os.path.basename(attach_file_name))
    encoders.encode_base64(payload) 
    payload.add_header('Content-Decomposition', 'attachment', filename=os.path.basename(attach_file_name))
    message.attach(payload)
    try: 
        #Create SMTP session for sending the mail
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) #use gmail with port
        session.starttls() #enable security
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD) #login with mail_id and password
        text = message.as_string()
        session.sendmail(GMAIL_USERNAME, GMAIL_RECEIVE, text)
        session.quit()
        print('Mail Sent success')
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise
try:
    time.sleep(2) # to stabilize sensor
    print("Camera Warning is ON")
    while True:
        if GPIO.input(23) == 0:
            print("Motion Detected")
            sleep(0.5)
            send_mail()
        time.sleep(5) #to avoid multiple detection
except:
    GPIO.cleanup()



