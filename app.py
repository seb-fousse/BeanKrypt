from flask import Flask, render_template, request
from forms import EncryptForm, DecryptForm
from werkzeug.utils import secure_filename
from beankrypting import encode, decode, generate_name
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
        path_to_bean_img = f'static/images/{bean_type}/{rand_int}.png'
        
        # Encode text into image
        #try:
        encoded_img = encode(path_to_bean_img, encrypt_form.text.data)
        #except Exception as e:
            #flash('Something went wrong when trying to encode your message')
            #print(e)
            
        # Save encoded image and display to user
        encoded_filename = f'{generate_name()}.png'
        encoded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], encoded_filename)
        encoded_img.save(encoded_filepath)

        return render_template('image.html', image_name=encoded_filename, image_path=encoded_filepath)

    return render_template('encrypt.html', form=encrypt_form)

@app.route("/decrypt", methods=['GET','POST'])
def decrypt():
    decrypt_form = DecryptForm()

    # On valid image submit
    if decrypt_form.validate_on_submit():

        print(request.files)
        image = request.files['image']

        # Save uploaded image temporarily
        filename = secure_filename(decrypt_form.image.data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Decode the image and keep track of the filepath and name
        try:
            decoded_img = decode(image)
        except Exception as e:
            flash('Something went wrong while trying to decrypt your image')
            print(e)

        # Save decoded image and display to user
        decoded_filename = f'decoded_{filename}'
        decoded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], decoded_filename)
        decoded_img.save(decoded_filepath)
        
        return render_template('image.html', image_name=decoded_filename, image_path=decoded_filepath)

    return render_template('decrypt.html', form=decrypt_form)