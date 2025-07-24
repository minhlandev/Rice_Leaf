# Rice Leaf Disease Identifier

Ứng dụng web sử dụng Deep Learning để nhận diện bệnh trên lá lúa từ ảnh. Người dùng có thể tải ảnh lá lúa lên, hệ thống sẽ xử lý và dự đoán loại bệnh (hoặc bình thường) dựa trên mô hình đã huấn luyện.

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Thông tin mô hình](#thông-tin-mô-hình)
- [Ghi chú](#ghi-chú)

---

## Giới thiệu

Dự án xây dựng hệ thống nhận diện bệnh lá lúa dựa trên ảnh, sử dụng mô hình deep learning (Keras/TensorFlow). Ứng dụng web phát triển bằng Flask, giao diện đơn giản, dễ sử dụng.

## Tính năng

- Nhận diện 4 lớp: Brown Spot, Leaf Blast, Leaf Blight, Normal.
- Tiền xử lý ảnh tự động (crop, resize, padding).
- Hiển thị ảnh preview và kết quả dự đoán.
- Giao diện web thân thiện, có video nền động.

## Cài đặt

### 1. Yêu cầu hệ thống

- Python 3.7+
- pip

### 2. Cài đặt thư viện

Cài đặt các thư viện cần thiết:
```sh
pip install -r setup.txt
```

### 3. Chuẩn bị mô hình

- Đảm bảo file `Fine_tune_Resep_cbam_BP_3th7_100_monitoring.keras` đã có trong thư mục gốc dự án.

### 4. Chạy ứng dụng

Chạy ứng dụng Flask:
```sh
python app.py
```
Ứng dụng sẽ chạy tại: http://localhost:5000

## Cách sử dụng

1. Truy cập trang web.
2. Nhấn "Select an image file" để chọn ảnh lá lúa từ máy tính.
3. Xem ảnh preview.
4. Nhấn "Predict" để nhận kết quả dự đoán.
5. Nhấn "Reset" để làm mới giao diện.

## Cấu trúc dự án

```
.
├── app.py
├── appec2.py
├── Fine_tune_Resep_cbam_BP_3th7_100_monitoring.keras
├── setup.txt
├── static/
│   ├── reset.js
│   ├── server.js
│   └── style.css
├── templates/
│   └── index.html
└── .gitignore
```

- [`app.py`](app.py): Flask app chạy local.
- [`appec2.py`](appec2.py): Flask app cho môi trường EC2 (đường dẫn model khác).
- [`setup.txt`](setup.txt): Danh sách thư viện cần cài đặt.
- [`static/style.css`](static/style.css): CSS giao diện.
- [`static/reset.js`](static/reset.js): JS xử lý preview ảnh và reset form.
- [`templates/index.html`](templates/index.html): Giao diện chính.

## Thông tin mô hình

- Mô hình Keras có custom layer CBAM, cần custom_objects khi load.
- Ảnh được crop tự động theo vùng lá, resize và padding về kích thước 224x224.
- Tiền xử lý sử dụng OpenCV.

## Ghi chú

- Nếu chạy trên server (EC2), dùng file [`appec2.py`](appec2.py) và chỉnh lại đường dẫn model cho phù hợp.
- Thư mục `upload/` sẽ được tạo tự động nếu cần (hiện tại không lưu ảnh upload).
- File [`static/server.js`](static/server.js) không cần thiết cho luồng hiện tại, có thể bỏ qua.

---

**Chúc bạn sử dụng hiệu quả!**
