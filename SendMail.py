from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import os

def send(host, port, from_mail, mail_password, html, subject, file, ttls, ssl):

	try:

		participant = pd.read_csv("../CreatCertifica/File/{}".format(file))

	except:

		return "We couldn't find the .csv file :(, please check again if it's uploaded."

	try:
		participant["Email"][0]
	except:
		
		return "We could not find the column named \"Email\" in the .csv file. Please create this column if it is not available and enter the contact emails under this column."


	try:

		if ttls:

			s = smtplib.SMTP(host=host, port=int(port))
			s.ehlo()
			s.starttls()
		elif ssl:
			server_ssl = smtplib.SMTP_SSL(host=host, port=int(port))
			server_ssl.ehlo()

	except:

		return "Incorrect host or port, please check."

	try:
		s.login(from_mail, mail_password)

	except:

		return "Your email or password is incorrect, please check again."

	Tr2Eng = str.maketrans("çğıöşü", "cgiosu")

	for i in range(0, len(participant)):

		temp = html

		for j in participant.columns:

			temp = temp.replace('${}'.format(j), str(participant[j][i]))


		mail = participant["Email"][i]

		msg = MIMEMultipart()
		msg["From"] = from_mail
		msg["Subject"] = subject
		msg["To"] = mail

		body = MIMEText(temp, "html") # convert the body to a MIME compatible string
		msg.attach(body)
		text = msg.as_string()
		s.sendmail(msg["From"], msg["To"], text)

	os.system("rm ../CreatCertifica/File/{}".format(file))
	s.quit()
	return "True"