import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
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

def analyze_weekly_spending(df):
    """Phân tích chi tiêu theo tuần"""
    print(f"\n{Fore.BLUE}[2/4] Phân tích chi tiêu theo tuần{Style.RESET_ALL}")

    # Thêm cột tuần
    df['week'] = df['order_date'].dt.isocalendar().week
    df['year'] = df['order_date'].dt.isocalendar().year

    # Tính tổng chi tiêu theo tuần và customer_id
    weekly_spending = df.groupby(['customer_id', 'year', 'week'])['total_amount'].sum().reset_index()
    weekly_spending['week_label'] = weekly_spending['year'].astype(str) + '-W' + weekly_spending['week'].astype(str).str.zfill(2)

    print("\nMẫu chi tiêu theo tuần:")
    print(weekly_spending.head().to_string())

    print(f"\nThống kê chi tiêu theo tuần:")
    stats = weekly_spending.groupby('customer_id')['total_amount'].agg(['mean', 'min', 'max'])
    print(f"→ Chi tiêu trung bình/tuần: ${stats['mean'].mean():.2f}")
    print(f"→ Chi tiêu thấp nhất/tuần: ${stats['min'].min():.2f}")
    print(f"→ Chi tiêu cao nhất/tuần: ${stats['max'].max():.2f}")

    return weekly_spending

def analyze_customer_behavior(df):
    """Phân tích hành vi khách hàng"""
    print(f"\n{Fore.BLUE}[3/4] Phân tích hành vi khách hàng{Style.RESET_ALL}")

    customer_behavior = pd.DataFrame()

    # 1. Tổng số đơn hàng
    customer_behavior['total_orders'] = df.groupby('customer_id').size()

    # 2. Tổng chi tiêu
    customer_behavior['total_spending'] = df.groupby('customer_id')['total_amount'].sum()

    # 3. Số loại sản phẩm (dựa trên giá và số lượng)
    df['product_type'] = df['price'].astype(str) + '_' + df['quantity'].astype(str)
    customer_behavior['unique_products'] = df.groupby('customer_id')['product_type'].nunique()

    # Thêm thống kê bổ sung
    customer_behavior['avg_order_value'] = customer_behavior['total_spending'] / customer_behavior['total_orders']

    print("\nThống kê hành vi khách hàng:")
    print(customer_behavior.to_string())

    print("\nTổng quan:")
    print(f"→ Trung bình số đơn hàng/khách: {customer_behavior['total_orders'].mean():.0f}")
    print(f"→ Trung bình chi tiêu/khách: ${customer_behavior['total_spending'].mean():.2f}")
    print(f"→ Trung bình số loại SP/khách: {customer_behavior['unique_products'].mean():.0f}")

    return customer_behavior

def analyze_monthly_trends(df):
    """Phân tích xu hướng theo tháng"""
    print(f"\n{Fore.BLUE}[4/4] Phân tích xu hướng theo tháng{Style.RESET_ALL}")

    # Thêm cột tháng
    df['year_month'] = df['order_date'].dt.to_period('M')

    # Tính số đơn hàng theo tháng cho mỗi khách hàng
    monthly_orders = df.groupby(['customer_id', 'year_month']).size().reset_index(name='num_orders')

    # Sắp xếp theo customer_id và tháng
    monthly_orders = monthly_orders.sort_values(['customer_id', 'year_month'])

    # Tìm khách hàng có số đơn giảm liên tiếp trong 3 tháng
    declining_customers = []

    for customer in monthly_orders['customer_id'].unique():
        customer_data = monthly_orders[monthly_orders['customer_id'] == customer]

        if len(customer_data) >= 3:
            # Tính sự thay đổi giữa các tháng liên tiếp
            for i in range(len(customer_data) - 2):
                orders_3m = customer_data['num_orders'].iloc[i:i+3].values
                if all(orders_3m[i] > orders_3m[i+1] for i in range(2)):
                    declining_customers.append({
                        'customer_id': customer,
                        'period': f"{customer_data['year_month'].iloc[i]} to {customer_data['year_month'].iloc[i+2]}",
                        'orders': orders_3m
                    })

    print("\nKhách hàng có số đơn giảm liên tiếp trong 3 tháng:")
    if declining_customers:
        for customer in declining_customers:
            print(f"\n→ {customer['customer_id']}:")
            print(f"   Giai đoạn: {customer['period']}")
            print(f"   Số đơn hàng: {customer['orders'][0]} → {customer['orders'][1]} → {customer['orders'][2]}")
    else:
        print("→ Không tìm thấy khách hàng nào")

    return declining_customers

def analyze_data(student_id=None):
    print(f"\n{Fore.GREEN}Bắt đầu phân tích dữ liệu...{Style.RESET_ALL}")
    print("=" * 50)

    if student_id is None:
        student_id = list_available_files()
        if student_id is None:
            return None

    # 1. Đọc dữ liệu
    df = load_data(student_id)

    # 2. Phân tích chi tiêu theo tuần
    weekly_spending = analyze_weekly_spending(df)

    # 3. Phân tích hành vi khách hàng
    customer_behavior = analyze_customer_behavior(df)

    # 4. Phân tích xu hướng theo tháng
    declining_customers = analyze_monthly_trends(df)

    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Hoàn thành phân tích dữ liệu!{Style.RESET_ALL}")

    return weekly_spending, customer_behavior, declining_customers

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        analyze_data(student_id)
    else:
        print("Usage: python analyze_data.py <student_id>")
