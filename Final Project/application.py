import smtplib
import sqlite3
from cs50 import SQL
from flask import Flask,render_template,request,redirect,session
import random

app = Flask(__name__)
app.secret_key = "AURORA"
name = "xxxx"
email = "xxxx"
password = "xxxx"
repassw = "xxxx"
otp = "xxxx"
logged_in = False
@app.route("/")
def home():
	if session.get("logged_in") == True :
		logged_in = True
		return render_template("home.html",logged_in = logged_in,name = name,shop = "Shop",sign = "Sign in")
	else:
		logged_in = False
		return render_template("home.html",logged_in = logged_in,sign = "Sign in")
			
	
@app.route("/register")
def register():
    logged_in = False
    return render_template("register.html",logged_in = logged_in,sign = "Sign in")
   
@app.route("/register_otp", methods =["POST"])
def register_otp():
    global name,email,password,repass,otp,logged_in,cart
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    repassw = request.form.get("repassword")
    otp = str(random.randint(100000,1000000))
    logged_in = False
    message = "Hey "+name+"\nYour 6 digit OTP is given below  \n"+otp
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login('avengerscoc6@gmail.com','I_AM_IRONMAN')
    server.sendmail('avengerscoc6@gmail.com',email,message)
    return render_template("otp.html",logged_in = logged_in, sign = "Sign in")
    
@app.route("/register_check",methods=["POST"])
def register_check():
	otpinput = request.form.get("otp")
	if otpinput == otp  :
		db = SQL("sqlite:///user.db")
		session["logged_in"] = True
		cart = 0
		db.execute("INSERT INTO users (Name,Email,Password,Cart) VALUES(?,?,?,?)",name , email , password,cart )
		message = "Congratulations "+name+"\nYou are registered in RAMAZON "
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login('avengerscoc6@gmail.com','I_AM_IRONMAN')
		server.sendmail('avengerscoc6@gmail.com',email,message)
		return redirect("/")
	else:
		logged_in = False
		return " Your OTP is incorrect"
	
@app.route("/login")
def login():
	logged_in = False
	return render_template("login.html",logged_in = logged_in,sign = "Sign in")
	
@app.route("/login_check",methods = ["POST"])
def login_check():
	global email, password, name, logged_in,cart
	db = SQL("sqlite:///user.db")
	email = request.form.get("email")
	password = request.form.get("password")
	row = db.execute("SELECT Id,Name,Password FROM users WHERE Email = ? AND Password = ?",email,password)
	if row[0]["Password"] == password :
		session["logged_in"] = True
		logged_in = True
		name = row[0]["Name"]
		return redirect("/")
	else:
		logged_in = False
		return redirect("/error")
		
@app.route("/error")
def error():
	return render_template("error.html",logged_in = logged_in,sign = "Sign in")
	
@app.route("/shop")
def shop():
	if session.get("logged_in") == True :
		logged_in = True
		db = SQL("sqlite:///user.db")
		return render_template("shop.html",logged_in = logged_in,name = name, shop = "Shop")
	else:
		return redirect("/")
		
@app.route("/cart", methods = ["POST"])
def cart():
	if session.get("logged_in") == True :
		logged_in = True
		db = SQL("sqlite:///user.db")
		if not request.form.get("mbp13") :
			mbp13 = 0
		else :
			mbp13 = int(request.form.get("mbp13")[1:])
		if not request.form.get("mba13") :
			mba13 = 0
		else :
			mba13 = int(request.form.get("mba13")[1:])
		if not request.form.get("mbp16") :
			mbp16 = 0
		else :
			mbp16 = int(request.form.get("mbp16")[1:])
		if not request.form.get("macmini") :
			macmini = 0
		else :
			macmini = int(request.form.get("macmini")[1:])
		if not request.form.get("imac21") :
			imac21 = 0
		else :
			imac21 = int(request.form.get("imac21")[1:])
		if not request.form.get("ipad7") :
			ipad7 = 0
		else :
			ipad7 = int(request.form.get("ipad7")[1:])
		if not request.form.get("prodxdr") :
			prodxdr = 0
		else :
			prodxdr = int(request.form.get("prodxdr")[1:])
		cart = mbp13 + mba13 + mbp16 + macmini + imac21 + ipad7 + prodxdr
		db.execute("UPDATE users SET Cart = ? WHERE Email = ? AND Password = ?",cart,email,password)
		return redirect("/profile")
	else :
		session["logged_in"] = False
		logged_in = False
		redirect("/")

@app.route("/profile")
def profile():
	if session.get("logged_in") == True :
		logged_in = True
		db = SQL("sqlite:///user.db")
		row= db.execute("SELECT Id,Name,Cart FROM users WHERE Email = ? AND Password = ?",email,password)
		cart = row[0]["Cart"]
		return render_template("profile.html",logged_in=logged_in,name = name,cart = cart, shop = "Shop")
	else :
		session["logged_in"] = False
		logged_in = False
		return redirect("/")
		
@app.route("/logout")
def logout():
	if session.get("logged_in") == True :
		session.pop("email", None)
		session["logged_in"] = False
		logged_in = False
		return redirect("/")

app.run(debug = True)