from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import pandas as pd
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def CreatCertifica(host, port, from_mail, mail_password, text_size, font, hexColor, height, subject, html, draftFile, listFile, number, ttls, ssl):

	try:

		participant = pd.read_csv("../CreatCertifica/File/{}".format(listFile))

	except:

		return "We couldn't find the .csv file :(, please check again if it's uploaded."


	try:

		pdf_main = PdfFileReader(open("../CreatCertifica/File/{}".format(draftFile), "rb"))
		page = pdf_main.getPage(0)
		width = page['/MediaBox'][2]
		height = page['/MediaBox'][3] - height

	except:

		return ".pdf draft certificate not found, please check again."

	try:
		participant["Email"][0]

	except:
		
		return "We could not find the column named \"Email\" in the .csv file. Please create this column if it is not available and enter the contact emails under this column."

	try:
		participant["Name"][0]
		
	except:
		
		return "We could not find the column named \"Name\" in the .csv file. Please create this column if it is not available and enter the names under this column."


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

	customColor = HexColor(hexColor)

	s = smtplib.SMTP(host=host, port=port)
	s.ehlo()
	s.starttls()
	s.login(from_mail, mail_password)

	Tr2Eng = str.maketrans("çğıöşü", "cgiosu")
	os.system("mkdir ../CreatCertifica/Certifica/{}/".format(number))

	for i in range(0, len(participant)):

		temp = html

		for j in participant.columns:

			temp = temp.replace('${}'.format(j), str(participant[j][i]))

		name = participant["Name"][i]
		name_eng = name.translate(Tr2Eng)
		mail = participant["Email"][i]

		pdf_main = PdfFileReader(open("../CreatCertifica/File/{}".format(draftFile), "rb"))
		page = pdf_main.getPage(0)
		width = page['/MediaBox'][2]

		packet = io.BytesIO()
		can = canvas.Canvas(packet, pagesize=letter)
		can.setFont(font, text_size)
		can.setFillColor(customColor)
		can.drawCentredString(int(width/2), int(height), name_eng)
		can.save()
		packet.seek(0)

		new_pdf = PdfFileReader(packet)
		output = PdfFileWriter()

		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)

		outputStream = open("../CreatCertifica/Certifica/{}/{}.pdf".format(number,name_eng), "wb")
		output.write(outputStream)
		outputStream.close()

		msg = MIMEMultipart()
		msg["From"] = from_mail
		msg["Subject"] = subject
		msg["To"] = mail

		body = MIMEText(temp, "html")
		msg.attach(body)

		filename = "../CreatCertifica/Certifica/{}/{}.pdf".format(number, name_eng)
		attachment = open(filename, "rb")
		p = MIMEBase('application', 'octet-stream')
		p.set_payload((attachment).read())
		encoders.encode_base64(p)  
		p.add_header('Content-Disposition', "attachment; filename= %s" % "{}.pdf".format(name_eng))
		msg.attach(p)

		text = msg.as_string()
		s.sendmail(msg["From"], msg["To"], text)

		os.system("rm ../CreatCertifica/Certifica/{}/{}.pdf".format(number, name_eng))

	os.system("rm ../CreatCertifica/File/{}".format(listFile))
	os.system("rm ../CreatCertifica/File/{}".format(draftFile))
	os.system("rm -R ../CreatCertifica/Certifica/{}".format(number))
	s.quit()

	return "True"

