import sys
import os
import pandas as pd
import numpy as np
from scipy import stats
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
    print(f"{Fore.BLUE}[1/4] Đọc dữ liệu{Style.RESET_ALL}")

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

    # Chỉ lấy dữ liệu tốt (không có NaN)
    df = df.dropna()

    # Tạo cột total_amount nếu chưa có
    if 'total_amount' not in df.columns:
        df['total_amount'] = round(df['quantity'] * df['price'] * (1 - df['discount']), 2)

    print(f"→ Đã đọc: {len(df):,} dòng")
    return df

def detect_zscore_anomalies(df, threshold=3):
    """Phát hiện bất thường bằng Z-score"""
    print(f"\n{Fore.BLUE}[2/4] Phát hiện bất thường bằng Z-score{Style.RESET_ALL}")

    z_scores = stats.zscore(df['total_amount'])
    zscore_anomalies = df[abs(z_scores) > threshold].copy()

    print(f"→ Số giao dịch bất thường (Z-score > {threshold}): {len(zscore_anomalies):,}")
    print(f"→ Tỷ lệ: {(len(zscore_anomalies)/len(df))*100:.2f}%")

    return zscore_anomalies

def detect_iqr_anomalies(df):
    """Phát hiện bất thường bằng IQR"""
    print(f"\n{Fore.BLUE}[3/4] Phát hiện bất thường bằng IQR{Style.RESET_ALL}")

    Q1 = df['total_amount'].quantile(0.25)
    Q3 = df['total_amount'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    iqr_anomalies = df[
        (df['total_amount'] < lower_bound) |
        (df['total_amount'] > upper_bound)
    ].copy()

    print(f"→ Số giao dịch bất thường (ngoài khoảng IQR): {len(iqr_anomalies):,}")
    print(f"→ Tỷ lệ: {(len(iqr_anomalies)/len(df))*100:.2f}%")
    print(f"\nPhạm vi bình thường:")
    print(f"→ Cận dưới: ${lower_bound:.2f}")
    print(f"→ Cận trên: ${upper_bound:.2f}")

    return iqr_anomalies

def detect_median_anomalies(df, multiplier=5):
    """Phát hiện bất thường dựa trên trung vị"""
    print(f"\n{Fore.BLUE}[4/4] Phát hiện bất thường dựa trên trung vị{Style.RESET_ALL}")

    median = df['total_amount'].median()
    median_anomalies = df[df['total_amount'] > median * multiplier].copy()

    print(f"→ Trung vị total_amount: ${median:.2f}")
    print(f"→ Ngưỡng phát hiện: ${median * multiplier:.2f}")
    print(f"→ Số giao dịch bất thường (> {multiplier} lần trung vị): {len(median_anomalies):,}")
    print(f"→ Tỷ lệ: {(len(median_anomalies)/len(df))*100:.2f}%")

    return median_anomalies

def analyze_and_save_anomalies(df, method_name, anomalies):
    """Phân tích và hiển thị thống kê về các giao dịch bất thường"""
    print(f"\n{Fore.YELLOW}Thống kê giao dịch bất thường ({method_name}):{Style.RESET_ALL}")
    print(f"→ Total amount trung bình: ${anomalies['total_amount'].mean():.2f}")
    print(f"→ Total amount thấp nhất: ${anomalies['total_amount'].min():.2f}")
    print(f"→ Total amount cao nhất: ${anomalies['total_amount'].max():.2f}")

    # Thêm cột để đánh dấu phương pháp phát hiện
    anomalies['detection_method'] = method_name

    return anomalies

def detect_anomalies(student_id=None):
    print(f"\n{Fore.GREEN}Bắt đầu phát hiện giao dịch bất thường...{Style.RESET_ALL}")
    print("=" * 50)

    # Nếu không có student_id, hiển thị danh sách file để chọn
    if student_id is None:
        student_id = list_available_files()
        if student_id is None:
            return None

    # 1. Đọc dữ liệu
    df = load_data(student_id)

    # 2. Phát hiện bất thường bằng các phương pháp khác nhau
    zscore_anomalies = detect_zscore_anomalies(df)
    iqr_anomalies = detect_iqr_anomalies(df)
    median_anomalies = detect_median_anomalies(df)

    # 3. Phân tích và gộp kết quả
    all_anomalies = pd.concat([
        analyze_and_save_anomalies(df, "Z-score", zscore_anomalies),
        analyze_and_save_anomalies(df, "IQR", iqr_anomalies),
        analyze_and_save_anomalies(df, "Median", median_anomalies)
    ])

    # 4. Loại bỏ các giao dịch trùng lặp và sắp xếp theo total_amount
    all_anomalies = all_anomalies.drop_duplicates(subset=['customer_id', 'order_date', 'total_amount'])
    all_anomalies = all_anomalies.sort_values('total_amount', ascending=False)

    # 5. Lưu kết quả
    output_file = os.path.join('output', f'suspect_transactions_{student_id}.csv')
    all_anomalies.to_csv(output_file, index=False)

    print(f"\n{Fore.GREEN}Tổng kết:{Style.RESET_ALL}")
    print(f"→ Tổng số giao dịch bất thường (unique): {len(all_anomalies):,}")
    print(f"→ Đã lưu kết quả vào file: {output_file}")

    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Hoàn thành phát hiện giao dịch bất thường!{Style.RESET_ALL}")

    return all_anomalies

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        detect_anomalies(student_id)
    else:
        print("Usage: python detect_anomalies.py <student_id>")
