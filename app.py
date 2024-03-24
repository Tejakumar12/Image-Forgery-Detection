
from flask import Flask, render_template, request
import os
import cv2
import hashlib

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def md5_hash_file(file_path):
    # Calculate the MD5 hash of a file
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def are_images_similar(img_path1, img_path2):
    # Calculate MD5 hash of image content
    hash_img1 = md5_hash_file(img_path1)
    hash_img2 = md5_hash_file(img_path2)

    return hash_img1 == hash_img2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['POST'])
def files():
    if request.method == 'POST':
        img1 = request.files.get('upload1')
        img2 = request.files.get('upload2')

        if img1 and img2:
            # Ensure the 'uploads' directory exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # Save the uploaded files with unique filenames
            img1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'img1.jpg')
            img2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'img2.jpg')
            img1.save(img1_path)
            img2.save(img2_path)

            try:
                # Implement your image processing logic here
                are_similar = are_images_similar(img1_path, img2_path)

                if are_similar:
                    msg = "Images are similar with same hash."
                else:
                    msg = "Images are different because hash is not matching."

            except Exception as e:
                # Handle exceptions (e.g., image processing errors)
                msg = f"Error processing images: {str(e)}"
                are_similar = False

            finally:
                # Remove the uploaded files after processing
                os.remove(img1_path)
                os.remove(img2_path)

            return render_template('index.html', msg=msg)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
