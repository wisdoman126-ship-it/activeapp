from flask import Flask, render_template, request

app = Flask(__name__, template_folder="pkg/template", static_folder="pkg/static")


@app.get("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = (
        "Sign-in is not connected yet. Your credentials have not been saved."
        if request.method == "POST"
        else None
    )
    return render_template("login.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = (
        "Account creation is not connected yet. Your details have not been saved."
        if request.method == "POST"
        else None
    )
    return render_template("register.html", message=message)


@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.get("/cart")
def cart():
    return render_template("customer_cart.html")


@app.get("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)