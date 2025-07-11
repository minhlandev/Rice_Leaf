from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import tensorflow as tf
import os
from werkzeug.utils import secure_filename
import base64
from PIL import Image
from io import BytesIO

# Cấu hình thư mục upload và định dạng hợp lệ
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Khởi tạo Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Custom functions cho model (nếu dùng CBAM hoặc layer tự định nghĩa)
def reduce_mean_keepdims(x, axis=None, keepdims=True, **kwargs):
    return tf.reduce_mean(x, axis=axis, keepdims=keepdims)

def reduce_max_keepdims(x, axis=None, keepdims=True, **kwargs):
    return tf.reduce_max(x, axis=axis, keepdims=keepdims)

# Load mô hình huấn luyện
model = tf.keras.models.load_model(
    'Fine_tune_Resep_cbam_BP_3th7_100_monitoring.keras',
    custom_objects={
        'reduce_mean_keepdims': reduce_mean_keepdims,
        'reduce_max_keepdims': reduce_max_keepdims
    }
)

@app.route('/predict', methods=['POST'])
def predict():
    original_base64 = None

    # Kiểm tra xem có file trong request không
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Đọc và mã hóa ảnh gốc sang base64
        file_bytes = file.read()
        original_base64 = base64.b64encode(file_bytes).decode()

        # Bỏ lưu ảnh vào thư mục upload
        # filename = secure_filename(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # with open(filepath, 'wb') as f:
        #     f.write(file_bytes)

        try:
            # Đọc ảnh trực tiếp từ bytes
            img_array = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
                blurred = cv2.GaussianBlur(gray, (7, 7), 0)
                thresh = cv2.adaptiveThreshold(
                    blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY_INV, 21, 7
                )
                kernel = np.ones((7, 7), np.uint8)
                morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    c = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(c)
                    pad = int(0.3 * max(w, h))
                    x1 = max(x - pad, 0)
                    y1 = max(y - pad, 0)
                    x2 = min(x + w + pad, img_rgb.shape[1])
                    y2 = min(y + h + pad, img_rgb.shape[0])
                    img_crop = img_rgb[y1:y2, x1:x2]
                else:
                    img_crop = img_rgb

                # Resize và padding ảnh về 224x224
                h, w, _ = img_crop.shape
                scale = 224 / max(w, h)
                new_w, new_h = int(w * scale), int(h * scale)
                img_resized = cv2.resize(img_crop, (new_w, new_h), interpolation=cv2.INTER_AREA)

                pad_top = (224 - new_h) // 2
                pad_bottom = 224 - new_h - pad_top
                pad_left = (224 - new_w) // 2
                pad_right = 224 - new_w - pad_left

                img_letterbox = cv2.copyMakeBorder(
                    img_resized, pad_top, pad_bottom, pad_left, pad_right,
                    borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255]
                )

                # Tiền xử lý cho model
                img = img_letterbox.astype(np.float32) / 255.0
                img = np.expand_dims(img, axis=0)
            else:
                return jsonify({'error': 'Error: Image variable is empty or has no data.'})
        except Exception as e:
            return str(e)

    # Dự đoán bằng model
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)
    class_names = ['Brown_Spot', 'Leaf_Blast', 'Leaf_Blight', 'Normal']
    response = {'class': class_names[predicted_class[0]]}

    # Hiển thị ảnh và kết quả
    return render_template('index.html', result=response, preview=original_base64)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
