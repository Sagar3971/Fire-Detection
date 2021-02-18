import cv2
import smtplib
import imghdr
from email.message import EmailMessage
from playsound import playsound

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
mail_content = '''There is Fire Detected in your place '''
message = EmailMessage()

sender = 'sender@gmail.com'
receiver = 'reciver@gmail.com'
message['From'] = sender
message['To'] = receiver
message['Subject'] = 'ALERT ALERT ALERT'

img_counter = 0
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        print("fire is detected")
        playsound('audio.wav')
        img_name = "Capture_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{}".format(img_name))
        img_counter += 1

        with open(img_name, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
            message.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
        mail_server.login("sender@gmail.com", 'password') //special password 
        mail_server.send_message(message)
        mail_server.quit()
        print('Mail Sent')

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
