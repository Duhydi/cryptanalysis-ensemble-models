# BÁO CÁO ĐỀ TÀI  
## Cryptanalysis bằng Machine Learning và Ensemble Models

---

## 1. Giới thiệu

Trong lĩnh vực an toàn thông tin, **cryptanalysis** là quá trình phân tích ciphertext nhằm suy luận thông tin về plaintext hoặc thuật toán mã hóa được sử dụng.  
Thay vì trực tiếp giải mã, đề tài này tập trung vào bài toán **nhận diện loại mã hóa (cipher classification)** dựa trên các đặc trưng thống kê của ciphertext.

Đề tài áp dụng các kỹ thuật **Machine Learning** và **Ensemble Models** để phân loại các dạng mã hóa cổ điển.

---

## 2. Mục tiêu đề tài

- Xây dựng hệ thống tự động dự đoán loại mã hóa từ ciphertext
- Áp dụng các đặc trưng thống kê trong cryptanalysis
- So sánh nhiều mô hình Machine Learning
- Lựa chọn mô hình có độ chính xác và độ ổn định cao nhất
- Xây dựng demo dự đoán loại mã hóa

---

## 3. Phạm vi nghiên cứu

### 3.1 Các loại mã hóa được nghiên cứu
- Caesar Cipher
- Vigenère Cipher
- Playfair Cipher
- XOR Cipher
- Rail Fence (Zigzag) Cipher

### 3.2 Dữ liệu
- Plaintext tiếng Anh có nghĩa
- Ciphertext được sinh ngẫu nhiên từ plaintext
- Mỗi mẫu gồm:
  - plaintext
  - ciphertext
  - loại mã hóa
  - khóa mã hóa

---

## 4. Phương pháp thực hiện

### 4.1 Tiền xử lý dữ liệu
- Chuyển ciphertext về chữ thường
- Loại bỏ ký tự không thuộc a–z
- Chuẩn hóa định dạng dữ liệu đầu vào

---

### 4.2 Trích xuất đặc trưng (Feature Engineering)

Các đặc trưng được xây dựng dựa trên lý thuyết cryptanalysis cổ điển:

#### 4.2.1 Đặc trưng thống kê
- **Entropy**: đo mức độ ngẫu nhiên của ciphertext
- **Index of Coincidence (IC)**: xác suất hai ký tự trùng nhau
- **Chi-square statistic**: đo độ lệch phân bố chữ cái so với phân bố đều
- **Length**: độ dài ciphertext

#### 4.2.2 Đặc trưng nâng cao
- **min_chi_after_shift**: hỗ trợ nhận diện Caesar cipher
- **avg_shift_ic**: phát hiện chu kỳ khóa trong Vigenère
- **repeated_digrams**: số cặp ký tự lặp lại (đặc trưng của Playfair)
- **block_entropy_variance**: độ dao động entropy theo từng đoạn

#### 4.2.3 Đặc trưng tần suất
- Tần suất xuất hiện của 26 ký tự a–z

---

## 5. Mô hình Machine Learning

Các mô hình được triển khai và so sánh:

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest
- Extra Trees
- XGBoost
- LightGBM
- Stacking Ensemble Models

---

## 6. Kết quả thực nghiệm

Sau quá trình huấn luyện và đánh giá, mô hình **RandomForestClassifier** cho kết quả ổn định nhất.

### Lý do lựa chọn:
- Độ chính xác cao (~92–94%)
- Ít overfitting khi thêm đặc trưng
- Không yêu cầu chuẩn hóa dữ liệu
- Hiệu quả với đặc trưng thống kê và rời rạc

---

## 7. Demo hệ thống

Hệ thống demo cho phép:
- Nhập ciphertext bất kỳ
- Trích xuất đặc trưng
- Dự đoán loại mã hóa tương ứng

Chạy demo:
```bash
python app.py
