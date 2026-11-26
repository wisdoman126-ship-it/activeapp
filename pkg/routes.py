from flask import current_app, render_template, request,flash,url_for,redirect,make_response, session
from werkzeug.security import generate_password_hash,check_password_hash
from pkg import app
from pkg.models import User , db 
from sqlalchemy.exc import SQLAlchemyError
from email_validator import validate_email, EmailNotValidError
@app.route("/")
def home():
    return render_template("home.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("name")
        email_add = request.form.get("email")
        phone_num = request.form.get("phone")
        address = request.form.get("address")
        password = request.form.get("password")
        confirm_pass= request.form.get("confirm_password")
        if not fullname or not email_add or not password or not phone_num or not address:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("register"))
        if len(password) < 8 :
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for("register"))
        if confirm_pass != password :
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))
        existing_user = User.query.filter_by(email=email_add).first()
        if existing_user:
            flash("Email address already exists.", "error")
            return redirect(url_for("register"))
        try:
            valid = validate_email(email_add)
        except EmailNotValidError as e:
            flash("Email is not valid.", "error")
            return redirect(url_for("register"))   
        try :
            password_hash = generate_password_hash(password)
            new_user = User(
                full_name=fullname,
                email=email_add,
                phone=phone_num,
                address=address,
                password_hash=password_hash
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login")) 
        except SQLAlchemyError:
            db.rollback()
            flash ("An error occurred while registering. Please try again.", "error")
            return redirect(url_for("register"))
        
        
        
        
        
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_add = request.form.get("email")
        password = request.form.get("password")
        if not email_add or not password:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("login"))
        user = User.query.filter_by(email=email_add).first()
        if user and check_password_hash(user.password_hash,password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))
    
   
    return render_template("login.html")



@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.get("/cart")
def cart():
    return render_template("customer_cart.html")


@app.get("/admin")
def admin():
    return render_template("admin.html")

