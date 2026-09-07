# 🧧 Ai Được Lì Xì - Đố Vui Trí Tuệ AI

Ứng dụng đố vui trí tuệ sử dụng **Groq AI** tự động sinh câu hỏi theo từng độ tuổi cụ thể từ **mầm non 3 tuổi đến sinh viên Đại học**. Giao diện **Light Theme** vui nhộn, tươi sáng, thiếu nhi, hỗ trợ responsive hoàn hảo trên điện thoại, máy tính bảng và máy tính.

---

## 🌟 Tính Năng Chính

1. **Đúng 3 màn hình tinh gọn:**
   - **Màn hình 1 (Chọn tuổi):** Hiển thị danh sách từng độ tuổi riêng biệt: **U3, 4 Tuổi -> 17 Tuổi, 18+, 30+, 40+, 50+, 60+** với biểu tượng đáng yêu, màu sắc kẹo ngọt. **Chủ đề hoàn toàn tự do** (AI tự động đổi chủ đề liên tục không lặp lại).
   - **Màn hình 2 (Quizz):** Câu hỏi trắc nghiệm cùng **4 đáp án A, B, C, D** to rõ, dễ bấm, hỗ trợ cả phím tắt bàn phím (`A`, `B`, `C`, `D`).
   - **Màn hình 3 (Chúc mừng):** Hiệu ứng mở bao lì xì may mắn & pháo hoa confetti rực rỡ kèm nút bấm **"Quay Lại Chọn Tuổi"**.

2. **Cơ chế tiền Lì Xì:**
   - 🎯 **Trả lời ĐÚNG:** Nhận ngay **50.000 VNĐ (50k)**.
   - 🌸 **Trả lời SAI:** Nhận lì xì an ủi **5.000 VNĐ (5k)**.
   - Số tiền lì xì tích lũy hiển thị liên tục ở góc trên giao diện.

3. **Thiết kế & Hiệu ứng:**
   - **Giao diện Light Theme:** Tươi sáng, ngộ nghĩnh, phong cách hoạt hình thiếu nhi với bóng đổ mềm và các gam màu pastel rực rỡ.
   - **Âm thanh Web Audio API:** Tiếng click pop vui tai, âm thanh chúc mừng thắng cuộc và nốt nhạc vui nhộn (không cần file mp3 ngoài, có nút bật/tắt âm thanh).
   - **Pháo hoa Confetti:** Nổ tung rực rỡ khi mở bao lì xì may mắn.
   - **Responsive 100%:** Tương thích từ điện thoại màn hình nhỏ (iPhone/Android 360px), iPad đến màn hình máy tính lớn.

4. **Trí tuệ nhân tạo Groq AI:**
   - Tích hợp mô hình tốc độ cao (mặc định `qwen/qwen3.8-27b`).
   - Hỗ trợ 2 khóa API (`GROQ_API_KEY` và `GROQ_API_KEY_CHAT_BOT`) với cơ chế tự động chuyển đổi dự phòng khi gặp sự cố mạng hoặc hết quota.
   - Có sẵn ngân hàng câu hỏi dự phòng cho từng độ tuổi, đảm bảo app không bao giờ bị gián đoạn.

---

## 📁 Cấu Trúc Mã Nguồn

```
AiDuocLiXi/
├── .env                     # Cấu hình API keys và cổng server
├── .env.example             # Mẫu cấu hình môi trường
├── requirements.txt         # Danh sách thư viện Python
├── run.py                   # Script khởi chạy ứng dụng
├── app/
│   ├── config.py            # Quản lý cài đặt môi trường
│   ├── main.py              # FastAPI server & các API endpoints
│   ├── models/
│   │   └── quiz.py          # Pydantic schemas dữ liệu câu hỏi, độ tuổi, kết quả
│   ├── services/
│   │   ├── ai_generator.py  # Dịch vụ Groq AI prompt engineering & sinh câu hỏi
│   │   ├── question_bank.py # Danh sách độ tuổi 3-22+ & kho câu hỏi dự phòng
│   │   └── notifier.py      # Module gửi thông báo Telegram
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Giao diện Light theme, thiếu nhi, responsive
│   │   └── js/
│   │       └── app.js       # Bộ điều khiển 3 màn hình, âm thanh, confetti
│   └── templates/
│       └── index.html       # Template HTML 3 màn hình
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy

### 1. Cài đặt thư viện:
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường (`.env`):
File `.env` đã được cấu hình sẵn với thông tin của bạn:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_KEY_CHAT_BOT=your_backup_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b

PORT=8088
HOST=0.0.0.0
```

### 3. Khởi động ứng dụng:
```bash
./venv/bin/python3 run.py
```
Ứng dụng sẽ hoạt động tại: **`http://localhost:8088/`**

---

## 📱 Các API Chính

- `GET /`: Mở giao diện web app (3 màn hình).
- `GET /api/ages`: Lấy danh sách độ tuổi (3 đến 22+).
- `POST /api/quiz/generate`: Tạo câu hỏi cho độ tuổi (Body: `{"age": 4}`).
- `POST /api/quiz/submit`: Kiểm tra đáp án và nhận tiền lì xì (Body: `{"question_id": "...", "age": 4, "selected_option": "A", "correct_answer": "A"}`).
