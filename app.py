from flask import Flask, render_template, request
from forms import EncryptForm, DecryptForm
from werkzeug.utils import secure_filename
from beankrypting import encode, decode
from random import randint
import os

upload_path = 'static/images/uploaded'
secret_key = 'mysecret123'

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config["UPLOAD_FOLDER"] = upload_path

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/encrypt", methods=['GET','POST'])
def encrypt():
    encrypt_form = EncryptForm()

    # On submit
    if encrypt_form.validate_on_submit():

        # Find path to random bean img
        bean_type = encrypt_form.bean_type.data.lower()
        rand_int = str(randint(0,4))
        path_to_bean_img = f'/static/images/{bean_type}/{rand_int}.png'
        # Encode text into image
        encoded_img = encode(path_to_bean_img, encrypt_form.text.data)

    return render_template('encrypt.html', form=encrypt_form)

@app.route("/decrypt", methods=['GET','POST'])
def decrypt():
    decrypt_form = DecryptForm()

    if decrypt_form.validate_on_submit():
        filename = secure_filename(decrypt_form.image.data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        decrypt_form.image.data.save(filepath)
        print(filename)

        img, decoded_filepath, decoded_filename = decode(filepath, app.config['UPLOAD_FOLDER'])
        os.remove(filepath)

        return render_template('image.html', image_path=decoded_filepath, image_name=decoded_filename)

    return render_template('decrypt.html', form=decrypt_form)



if __name__ == '__main__':
    app.run()