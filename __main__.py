from datatools import Data, DataFilmu
from flask import *
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired
app = Flask(__name__)
UPLOAD_FOLDER = app.static_folder + "/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "CSRF"
def error_404(error):
	return render_template("404.html"), 404
app.register_error_handler(404, error_404)

class FileFormular(FlaskForm):
	soubor = FileField("Vlož obrázek", validators = [FileRequired()], render_kw = dict(class_ = "form-control"))
	submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))
class LoginForm(FlaskForm):
	user = StringField("Uživatel", validators = [InputRequired()], render_kw = dict(class_ = "form-control")) #Přihlašovací jméno
	password = PasswordField("Heslo", validators = [InputRequired()], render_kw = dict(class_ = "form-control")) #Heslo
	submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))
class RegisterForm(LoginForm): pass
class FilmForm(FlaskForm):
	nazev = StringField("Název filmu", validators = [InputRequired()], render_kw = dict(class_ = "form-control"))
	rezie = StringField("Režie", validators = [InputRequired()], render_kw = dict(class_ = "form-control"))
	zanr = StringField("Žánr", validators = [InputRequired()], render_kw = dict(class_ = "form-control"))
	submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))
data = Data()
dataFilmu = DataFilmu()

@app.route("/")
def index():
	username = ""
	try:
		username = request.cookies.get('userID')
	except:
		username = ""
	return render_template("index.html", user = username)

@app.route("/login", methods = ["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = form.user.data
		password = form.password.data
		je_spravne = data.login(user,password)[0]
		if je_spravne:
			resp = make_response(redirect(url_for("index")))
			resp.set_cookie('userID', user)
			return resp
		else:
			return render_template("login.html", form = form, user = "", spatne = True)
	try:
		user = request.cookies.get("userID")
	except:
		user = ""
	return render_template("login.html", form = form, user = user, spatne = False)	

@app.route("/register", methods = ["GET","POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = form.user.data
		password = form.password.data
		data.append(user,password)
		return redirect(url_for("index"))
	user = ""
	try:
		user = request.cookies.get('userID')
	except:
		user = ""
	return render_template("register.html", user = user, form = form)

@app.route("/galerie/", methods = ["GET", "POST"])
def galerie():
	form = FileFormular()
	if form.validate_on_submit():
		soubor = form.soubor.data
		nazev = secure_filename(soubor.filename)
		soubor.save(os.path.join(app.config['UPLOAD_FOLDER'], nazev))
	obrazky = os.listdir(app.static_folder + "/uploads")
	username = ""
	try:
		username = request.cookies.get('userID')
	except:
		username = ""
	return render_template("galerie.html", form = form, obrazky = obrazky, user = username)
@app.route("/odhlasitse")
def odhlasitse():
	resp = make_response(redirect(url_for("index")))
	resp.set_cookie('userID', '', expires=0)
	return resp
@app.route("/filmy", methods = ["GET","POST"])
def filmy():
	form = FilmForm()
	if form.validate_on_submit():
		nazev = form.nazev.data
		rezie = form.rezie.data
		zanr = form.zanr.data
		dataFilmu.append(nazev,rezie,zanr)
	filmy = []
	for i in dataFilmu.data:
		filmy.append(i[0])
	filmy = list(enumerate(filmy))
	try:
		username = request.cookies.get('userID')
	except:
		username = ""
	return render_template("filmy.html", user = username, form = form, filmy = filmy)	
@app.route("/detail_filmu/<int:idFilmu>")
def detail_filmu(idFilmu):
	film = dataFilmu[idFilmu]
	try:
		username = request.cookies.get('userID')
	except:
		username = ""
	return render_template("detail_filmu.html", user = username, nazev = film[0], rezie = film[1], zanr = film[2])	
app.run("0.0.0.0")