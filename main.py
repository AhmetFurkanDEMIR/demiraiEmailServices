from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from wtforms import StringField,TextAreaField, Form, validators,IntegerField,SelectField, PasswordField
from SendMail import send
from CreatCertifica import CreatCertifica
import os
import random
from flask_wtf.file import FileField

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = 'File'

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/BulkMail",methods = ["GET","POST"])
def BulkMail():

    form = MailForm(request.form)

    if request.method == "POST" and form.validate():

        title = form.title.data
        content = form.content.data
        mail = form.mail.data
        password = form.password.data
        host = form.host.data
        port = form.port.data

        try:
            ttls = request.form["TTLS"]
            ttls=True

        except:
            ttls = False

        try:
            ssl = request.form["SSL"]
            ssl = True

        except:
            ssl = False

        if ssl == False and ttls == False:

            flash("Choose only one of SSL or TTLS.","danger")
            return render_template("mail.html",form = form)

        elif ssl and ttls:

            flash("Choose only one of SSL or TTLS.","danger")
            return render_template("mail.html",form = form)

        flag = True
        strr=""
        while flag:
            flag = False
            strr = "Participant{}.csv".format(str(random.randint(0,10000)))
            for i in os.listdir("../CreatCertifica/File"):

                if i==strr:
                    flag = True
                    break
				
        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_PATH'], "{}".format(strr)))
        error = send(host, port, mail, password, content, title, strr, ttls, ssl)
        error = "True"
        if error!="True":

            flash(error,"danger")  
        else:
        	
            flash("Transaction successful, mails sent.","success")

        return render_template("mail.html",form = form)

    return render_template("mail.html",form = form)


@app.route("/CertificateGeneration",methods=["GET", "POST"])
def CertificateGeneration():
	
    form = formCer(request.form)

    if request.method == "POST":

        title = form.title.data
        content = form.content.data
        mail = form.mail.data
        password = form.password.data
        host = form.host.data
        port = form.port.data
        font_size = form.punto.data
        font = form.font.data
        color = request.form["renk"]
        v = form.v.data

        try:
            ttls = request.form["TTLS"]
            ttls=True

        except:
            ttls = False

        try:
            ssl = request.form["SSL"]
            ssl = True

        except:
            ssl = False

        if ssl == False and ttls == False:

            flash("Choose only one of SSL or TTLS.","danger")
            return render_template("CreatCer.html",form = form)

        elif ssl and ttls:

            flash("Choose only one of SSL or TTLS.","danger")
            return render_template("CreatCer.html",form = form)

        flag = True
        strr=""
        strr1=""
        while flag:
            flag = False
            intt = str(random.randint(0,10000))
            strr = "Participant{}.csv".format(intt)
            strr1 = "Draft{}.pdf".format(intt)
            for i in os.listdir("../CreatCertifica/File"):

                if i==strr and i==strr1:
                    flag = True
                    break

        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_PATH'], strr))

        fileDraft = request.files["draft"]
        fileDraft.save(os.path.join(app.config['UPLOAD_PATH'], strr1))

        error = CreatCertifica(host, port, mail, password, font_size, font, color, v, title, content, strr1, strr, intt, ttls, ssl)

        if error!="True":

            flash(error,"danger")  
        else:
        	
            flash("Transaction successful, certificates created and sent.","success")

        return render_template("CreatCer.html",form = form)

    return render_template("CreatCer.html",form = form)


class MailForm(Form):

    default = " Hello $Name, how are you doing ?. This text is specific to this $Email"

    title = StringField("Subject",validators=[validators.Length(min = 5,max = 100)])
    content = TextAreaField("Text",validators=[validators.Length(min = 10)], default=default)
    mail = StringField("E-mail",validators=[validators.email()])
    password = PasswordField("Password",)
    file = FileField("E-mail list")
    host = StringField("Host", default="smtp.gmail.com")
    port = StringField("Port", default="587")

class formCer(Form):

    default = " Hello $Name, how are you doing ?. This text is specific to this $Email"

    title = StringField("Subject",validators=[validators.Length(min = 5,max = 100)])
    content = TextAreaField("Text",validators=[validators.Length(min = 10)], default=default)
    file = FileField("E-mail list")
    punto = IntegerField("Font Size", validators=[validators.NumberRange(min=1, max=200, message='Invalid length')])
    font = SelectField("Font",choices = 
                    [("Times New Roman","Times New Roman"),
					("Helvetica","Helvetica"),
					("Verdana","Verdana"),
					("Courier","Courier"),
					("Optina","Optina"),
					("Monaco","Monaco"),
					("Didot","Didot"),
					("Copperplate","Copperplate"),
					("Lucida","Lucida"),
					("Perpetua","Perpetua"),
					("Candara","Candara"),
					("Garamond","Garamond"),
					("Comic","Comic")])
    v = IntegerField("Vertical position of the name from above (px)")
    
    draft = FileField("Draft Certificate")
    mail = StringField("E-mail")
    password = PasswordField("Password")
    host = StringField("Host", default="smtp.gmail.com")
    port = StringField("Port", default="587")

if __name__ == "__main__":
    app.run(debug=True)