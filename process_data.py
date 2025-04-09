import sys
import os
import pandas as pd
import numpy as np
from colorama import init, Fore, Style

init()

def list_available_files():
    """Liệt kê các file dữ liệu có sẵn"""
    files = [f for f in os.listdir('output') if f.startswith('transactions_')]
    if not files:
        print(f"\n{Fore.RED}Không tìm thấy file dữ liệu nào trong thư mục output!{Style.RESET_ALL}")
        return None

    print(f"\n{Fore.YELLOW}Danh sách file dữ liệu:{Style.RESET_ALL}")
    for i, file in enumerate(files, 1):
        file_path = os.path.join('output', file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        print(f"{i}. {file} ({file_size:.1f} MB)")

    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}Chọn file để phân tích (1-{len(files)}): {Style.RESET_ALL}")
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx].replace('transactions_', '').replace('.csv', '')
        except ValueError:
            pass
        print(f"{Fore.RED}Lựa chọn không hợp lệ!{Style.RESET_ALL}")

def load_data(student_id):
    """Đọc và chuẩn bị dữ liệu"""
    print(f"{Fore.BLUE}[1/5] Đọc dữ liệu từ file CSV{Style.RESET_ALL}")

    input_file = os.path.join('output', f'transactions_{student_id}.csv')
    print(f"File: {input_file}")

    df = pd.read_csv(input_file,
                    dtype={
                        'customer_id': str,
                        'price': float,
                        'quantity': int,
                        'discount': float
                    },
                    parse_dates=['order_date'])

    print(f"→ Đọc thành công {len(df):,} dòng")

    print("\nCấu trúc dữ liệu:")
    print(df.dtypes)
    return df

def calculate_total(df):
    """Tính toán total_amount"""
    print(f"\n{Fore.BLUE}[2/5] Tính toán total_amount{Style.RESET_ALL}")

    # Tạo cột total_amount nếu chưa có
    if 'total_amount' not in df.columns:
        df['total_amount'] = round(df['quantity'] * df['price'] * (1 - df['discount']), 2)

    print("→ Đã tạo cột total_amount")

    print("\nThống kê cột total_amount:")
    print(f"Giá trị thấp nhất: ${df['total_amount'].min():.2f}")
    print(f"Giá trị cao nhất: ${df['total_amount'].max():.2f}")
    print(f"Giá trị trung bình: ${df['total_amount'].mean():.2f}")
    return df

def separate_data(df):
    """Tách dữ liệu thành good và bad"""
    print(f"\n{Fore.BLUE}[3/5] Phân tách dữ liệu tốt và xấu{Style.RESET_ALL}")

    # Lọc ra các dòng có lỗi (null hoặc giá trị không hợp lệ)
    bad_rows = df[
        df['price'].isna() |
        df['quantity'].isna() |
        df['discount'].isna() |
        df['total_amount'].isna()
    ]

    # Lọc ra các dòng dữ liệu tốt
    good_rows = df[
        df['price'].notna() &
        df['quantity'].notna() &
        df['discount'].notna() &
        df['total_amount'].notna()
    ]

    print("Thống kê dữ liệu:")
    print(f"→ Số dòng tốt: {len(good_rows):,} ({len(good_rows)/len(df)*100:.2f}%)")
    print(f"→ Số dòng xấu: {len(bad_rows):,} ({len(bad_rows)/len(df)*100:.2f}%)")
    return good_rows, bad_rows

def save_bad_rows(bad_rows, student_id):
    """Lưu các dòng lỗi ra file"""
    print(f"\n{Fore.BLUE}[4/5] Lưu dữ liệu lỗi{Style.RESET_ALL}")

    output_file = os.path.join('output', f'bad_rows_{student_id}.csv')
    bad_rows.to_csv(output_file, index=False)
    print(f"→ Đã lưu {len(bad_rows):,} dòng lỗi vào file: {output_file}")

def display_samples(good_rows, bad_rows):
    """Hiển thị mẫu dữ liệu"""
    print(f"\n{Fore.BLUE}[5/5] Hiển thị mẫu dữ liệu{Style.RESET_ALL}")

    print("\nMẫu dữ liệu tốt (5 dòng đầu):")
    print("=" * 80)
    print(good_rows.head().to_string())

    print("\nMẫu dữ liệu xấu (5 dòng đầu):")
    print("=" * 80)
    print(bad_rows.head().to_string())

def process_data(student_id=None):
    print(f"\n{Fore.GREEN}Bắt đầu xử lý dữ liệu...{Style.RESET_ALL}")
    print("=" * 50)

    # Nếu không có student_id, hiển thị danh sách file để chọn
    if student_id is None:
        student_id = list_available_files()
        if student_id is None:
            return None, None

    # 1. Đọc dữ liệu
    df = load_data(student_id)

    # 2. Tính total_amount
    df = calculate_total(df)

    # 3. Tách dữ liệu
    good_rows, bad_rows = separate_data(df)

    # 4. Lưu dữ liệu lỗi
    save_bad_rows(bad_rows, student_id)

    # 5. Hiển thị mẫu
    display_samples(good_rows, bad_rows)

    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Hoàn thành xử lý dữ liệu!{Style.RESET_ALL}")

    return good_rows, bad_rows

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        process_data(student_id)
    else:
        process_data()
