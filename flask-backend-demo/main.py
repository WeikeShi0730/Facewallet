from flask import Flask, render_template

app = Flask("__main__")


@app.route("/")
def my_index():
    return render_template("index.html", token="flask-react-demo")

@app.route("/register")
def register():
    return 

@app.route("/payment")
def payment():
    return

app.run(debug=True)
