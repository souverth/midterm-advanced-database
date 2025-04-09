# CopyRight Nguyễn Trọng Kiên

Đây là bài tập lớn giữa kì môn cơ sở dữ liệu nâng cao.

# Run

python main.py

# Hệ Thống Phân Tích Dữ Liệu

Dự án này cung cấp một bộ công cụ toàn diện để xử lý và phân tích dữ liệu, với khả năng phát hiện bất thường và tạo báo cáo chi tiết.

## Tính Năng Chính

- **Xử lý Dữ liệu**: Làm sạch và chuẩn hóa dữ liệu đầu vào
- **Phân Tích Nâng Cao**: Thực hiện các phân tích chuyên sâu trên dữ liệu
- **Phát Hiện Bất Thường**: Nhận diện các mẫu và giao dịch đáng ngờ
- **Tạo Dữ Liệu**: Công cụ tạo dữ liệu mẫu cho mục đích kiểm thử
- **Báo Cáo Tự Động**: Xuất báo cáo dưới dạng CSV và hình ảnh trực quan

## Cấu Trúc Thư Mục

```
.
├── main.py                 # File chính điều khiển luồng xử lý
├── process_data.py         # Module xử lý và làm sạch dữ liệu
├── analyze_data.py         # Module phân tích dữ liệu cơ bản
├── advanced_analysis.py    # Module phân tích nâng cao
├── detect_anomalies.py     # Module phát hiện bất thường
├── generate_data.py        # Công cụ tạo dữ liệu mẫu
├── img/                    # Thư mục chứa hình ảnh kết quả
└── output/                 # Thư mục chứa file kết quả CSV
```

## File Kết Quả

Hệ thống tạo ra các loại file kết quả sau:

- **Giao dịch đáng ngờ**: `suspect_transactions_[ID].csv`
- **Mẫu hàng ngày**: `daily_patterns_[ID].csv`
- **Dòng dữ liệu lỗi**: `bad_rows_[ID].csv`
- **Giao dịch đã xử lý**: `transactions_[ID].csv`
- **Biểu đồ phân cụm**: `img/daily_patterns_clusters_[ID].png`

## Hướng Dẫn Sử Dụng

1. Chạy chương trình chính:

```bash
python main.py
```

2. Các kết quả sẽ được tạo ra trong thư mục `output/` và `img/`

## Yêu Cầu Hệ Thống

- Python 3.x
- Các thư viện cần thiết (được liệt kê trong requirements.txt)

## Liên Hệ Hỗ Trợ

Nếu bạn gặp vấn đề hoặc cần hỗ trợ, vui lòng tạo issue trên repository.
