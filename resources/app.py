# face_auth_app/app.py

import os
import cv2
import numpy as np
from deepface import DeepFace
from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

EMBEDDINGS_PATH = "embeddings/"
os.makedirs(EMBEDDINGS_PATH, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_embedding(image_path):
    try:
        embedding = DeepFace.represent(img_path=image_path, model_name='Facenet')[0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print("Embedding error:", e)
        return None

def save_embedding(username, embedding):
    with open(f"{EMBEDDINGS_PATH}{username}.pkl", "wb") as f:
        pickle.dump(embedding, f)

def load_embedding(username):
    try:
        with open(f"{EMBEDDINGS_PATH}{username}.pkl", "rb") as f:
            return pickle.load(f)
    except:
        return None

def verify_face(embedding1, embedding2, threshold=0.7):
    from scipy.spatial.distance import cosine
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity >= threshold, similarity

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    file = request.files["photo"]

    if file.filename == '' or not allowed_file(file.filename):
        flash("Invalid file type. Only PNG and JPEG images are allowed.", "danger")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = f"temp_{username}.{filename.rsplit('.', 1)[1]}"
    file.save(filepath)

    embedding = extract_embedding(filepath)
    os.remove(filepath)

    if embedding is not None:
        save_embedding(username, embedding)
        flash("User registered successfully.", "success")
    else:
        flash("Face not detected.", "danger")
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    file = request.files["photo"]

    if file.filename == '' or not allowed_file(file.filename):
        flash("Invalid file type. Only PNG and JPEG images are allowed.", "danger")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = f"temp_login.{filename.rsplit('.', 1)[1]}"
    file.save(filepath)

    input_embedding = extract_embedding(filepath)
    stored_embedding = load_embedding(username)
    os.remove(filepath)

    if input_embedding is not None and stored_embedding is not None:
        matched, score = verify_face(input_embedding, stored_embedding)
        if matched:
            flash(f"Authentication successful. Similarity: {score:.2f}", "success")
        else:
            flash(f"Authentication failed. Similarity: {score:.2f}", "danger")
    else:
        flash("Face not detected or user not found.", "danger")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
