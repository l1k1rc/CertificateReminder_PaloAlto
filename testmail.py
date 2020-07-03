#!/usr/bin/env python3
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

strFrom = 'PaloAltoCert@noreply.com'
strTo = 'grosraton@corp.com'

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'Mail debug'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'RaccoonCorporate'

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

# Accept the HTML format
os.system('python ParseXML.py')
htmlF = open("data/data_mail.html")
msgText = MIMEText(htmlF.read(), 'html')
msgAlternative.attach(msgText)
# For the OK picture
fp = open('data/ok.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image2>')
msgRoot.attach(msgImage)

# For the NO picture
fp = open('data/cross.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image3>')
msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
smtp = smtplib.SMTP()
smtp.connect('localhost')
smtp.set_debuglevel(1)
# smtp.login('exampleuser', 'examplepass')
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()
