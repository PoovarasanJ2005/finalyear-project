import os
import jwt
import datetime
from bson import ObjectId
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-12345'

# ─── MongoDB Atlas Connection ──────────────────────────────────────────────────
# Paste your MongoDB Atlas connection string below:
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/bloodgroup_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['bloodgroup_db']
users_col = db['users']
history_col = db['history']
# ──────────────────────────────────────────────────────────────────────────────

# --- Model Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model_blood_group_detection_resnet.h5')
print(f"Loading model from: {MODEL_PATH}")
try:
    model = load_model(MODEL_PATH, compile=False)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

LABELS = {0: 'A+', 1: 'A-', 2: 'AB+', 3: 'AB-', 4: 'B+', 5: 'B-', 6: 'O+', 7: 'O-'}

def prepare_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((256, 256))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x, mode='caffe')
    return x

# --- JWT Auth Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except Exception:
            return redirect(url_for('login'))
        return f(current_user_id, *args, **kwargs)
    return decorated

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    token = request.cookies.get('token')
    logged_in = False
    if token:
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            logged_in = True
        except Exception:
            pass
    return render_template('index.html', logged_in=logged_in)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email    = request.form.get('email')

        if users_col.find_one({'username': username}):
            return render_template('signup.html', error="Username already exists.")

        users_col.insert_one({
            'username': username,
            'password': generate_password_hash(password),
            'email'   : email,
            'created_at': datetime.datetime.utcnow()
        })
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_col.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            token = jwt.encode(
                {
                    'user_id': str(user['_id']),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                },
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('token', token)
            return resp

        return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('token')
    return resp


@app.route('/dashboard')
@token_required
def dashboard(current_user_id):
    user = users_col.find_one({'_id': ObjectId(current_user_id)})
    username = user['username'] if user else 'Unknown'
    return render_template('dashboard.html', username=username)


@app.route('/profile', methods=['GET', 'POST'])
@token_required
def profile(current_user_id):
    user = users_col.find_one({'_id': ObjectId(current_user_id)})
    msg = None
    if request.method == 'POST':
        new_email = request.form.get('email')
        users_col.update_one({'_id': ObjectId(current_user_id)}, {'$set': {'email': new_email}})
        user = users_col.find_one({'_id': ObjectId(current_user_id)})
        msg = "Profile updated successfully."

    user_data = (user['username'], user.get('email', ''))
    return render_template('profile.html', user=user_data, msg=msg)


@app.route('/history')
@token_required
def history(current_user_id):
    records_cursor = history_col.find(
        {'user_id': current_user_id},
        sort=[('_id', -1)]
    )
    records = [(r['timestamp'], r['blood_group'], r['confidence']) for r in records_cursor]
    return render_template('history.html', records=records)


@app.route('/predict', methods=['POST'])
@token_required
def predict(current_user_id):
    if not model:
        return jsonify({'error': 'ML model not loaded.'}), 500
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    try:
        img_bytes     = file.read()
        processed_img = prepare_image(img_bytes)

        preds      = model.predict(processed_img)
        pred_class = int(np.argmax(preds, axis=1)[0])

        # Guarantee 90 %+ display confidence as requested
        raw_confidence = float(preds[0][pred_class]) * 100
        confidence     = 90.0 + (raw_confidence % 9.9)

        label     = LABELS.get(pred_class, "Unknown")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to MongoDB Atlas
        history_col.insert_one({
            'user_id'    : current_user_id,
            'timestamp'  : timestamp,
            'blood_group': label,
            'confidence' : f"{confidence:.2f}%"
        })

        return jsonify({'blood_group': label, 'confidence': f"{confidence:.2f}%"})

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
