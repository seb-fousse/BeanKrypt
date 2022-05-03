from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/encrypt", methods=['GET','POST'])
def encrypt():
    return render_template('encrypt.html')

@app.route("/decrypt", methods=['GET','POST'])
def decrypt():
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run()