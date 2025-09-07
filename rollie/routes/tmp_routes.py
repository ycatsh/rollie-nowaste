import random
import io
import base64

from flask import (
    render_template, request, jsonify
)
import tensorflow as tf
import numpy as np
from PIL import Image

from rollie import app, db
from rollie.models import User, ScanIn
from rollie.enums import TrashType
from rollie.utils.helper import (
    validate_scanned_qr, time_now_ist
)


@app.route('/tmp/scan', methods=['POST', 'GET'])
def scan(): 
    return render_template('tmp/scan.html', title="Scanner")


@app.route('/tmp/validate_qr', methods=['POST'])
def validate_qr():
    data = request.get_json()
    scanned_id = data.get("unique_id", "").strip()

    if not validate_scanned_qr(scanned_id):
        return jsonify({"success": False, "message": "Invalid Key Card."}), 400

    user = User.query.filter_by(unique_id=scanned_id).first()
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    scanin = ScanIn(
        user_id=user.id, 
        weight=random.randint(1, 10), 
        type=random.choice([
            TrashType.ORGANIC,
            TrashType.PAPER,
            TrashType.HOUSEHOLD
        ]),
        timestamp=time_now_ist()
    )
    db.session.add(scanin)
    db.session.commit()

    return jsonify({"success": True, "message": "BIN OPEN"}), 200


MODEL_PATH = "models/garbage_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/tmp/garbage")
def classifier():
    return render_template("tmp/classifier.html", title="Scanner")

@app.route("/tmp/garbage/predict", methods=["POST"])
def garbage_predict():
    try:
        data = request.get_json(force=True)
        if "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = data["image"]
        image_bytes = base64.b64decode(image_data.split(",")[1])
        img_array = preprocess_image(image_bytes)
        
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        predicted_class = CLASS_NAMES[np.argmax(score)]
        confidence = float(np.max(score))
        
        return jsonify({
            "class": predicted_class,
            "confidence": round(confidence * 100, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

