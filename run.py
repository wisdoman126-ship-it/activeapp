from flask import Flask, render_template

app = Flask(__name__, template_folder="pkg/template", static_folder="pkg/static")


@app.get("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)