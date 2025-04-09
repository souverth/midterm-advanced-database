import pandas as pd
import numpy as np
import random
import sys
import os
from colorama import init, Fore, Style

init()  # Khởi tạo colorama

def create_product_names(num_records):
    """Tạo danh sách tên sản phẩm ngẫu nhiên"""
    print(f"\n{Fore.BLUE}[1/7] Tạo tên sản phẩm{Style.RESET_ALL}")

    product_names = [f'Product_{i}' for i in range(1, num_records + 1)]
    random.shuffle(product_names)  # Xáo trộn danh sách để tạo tính ngẫu nhiên

    print(f"→ Đã tạo {num_records:,} tên sản phẩm ngẫu nhiên")
    return product_names

def create_customer_ids(student_id, num_records):
    """Tạo danh sách customer IDs"""
    print(f"{Fore.BLUE}[2/7] Tạo customer IDs{Style.RESET_ALL}")
    customer_ids = [f'STD_{student_id}'] * num_records
    print(f"→ Đã tạo {num_records:,} customer IDs cho sinh viên {student_id}")
    return customer_ids

def create_order_dates(num_records):
    """Tạo chuỗi thời gian"""
    print(f"\n{Fore.BLUE}[3/7] Tạo chuỗi thời gian{Style.RESET_ALL}")
    order_dates = pd.date_range(start='2022-01-01', periods=num_records, freq='H')
    print("Thông tin chuỗi thời gian:")
    print(f"→ Thời gian bắt đầu: {order_dates[0]}")
    print(f"→ Thời gian kết thúc: {order_dates[-1]}")
    print(f"→ Tần suất: Mỗi giờ")
    print(f"→ Số lượng mốc thời gian: {len(order_dates):,}")
    return order_dates

def create_prices(num_records):
    """Tạo giá sản phẩm"""
    print(f"\n{Fore.BLUE}[4/7] Tạo giá sản phẩm{Style.RESET_ALL}")
    prices = np.round(np.random.uniform(1.0, 100.0, num_records), 2)
    print("Thống kê giá:")
    print(f"→ Giá thấp nhất: ${np.min(prices):.2f}")
    print(f"→ Giá cao nhất: ${np.max(prices):.2f}")
    print(f"→ Giá trung bình: ${np.mean(prices):.2f}")
    return prices

def create_quantities(num_records):
    """Tạo số lượng sản phẩm"""
    print(f"\n{Fore.BLUE}[5/7] Tạo số lượng sản phẩm{Style.RESET_ALL}")
    quantities = np.random.randint(1, 10, num_records)
    print("Thống kê số lượng:")
    print(f"→ Số lượng thấp nhất: {np.min(quantities)}")
    print(f"→ Số lượng cao nhất: {np.max(quantities)}")
    print(f"→ Số lượng trung bình: {np.mean(quantities):.1f}")
    return quantities

def create_discounts(num_records):
    """Tạo giảm giá"""
    print(f"\n{Fore.BLUE}[6/7] Tạo giảm giá{Style.RESET_ALL}")
    discounts = np.round(np.random.uniform(0.0, 0.5, num_records), 2)
    print("Thống kê giảm giá:")
    print(f"→ Giảm giá thấp nhất: {np.min(discounts):.2%}")
    print(f"→ Giảm giá cao nhất: {np.max(discounts):.2%}")
    print(f"→ Giảm giá trung bình: {np.mean(discounts):.2%}")
    return discounts

def add_errors(prices, num_records):
    """Thêm lỗi vào dữ liệu"""
    print(f"\n{Fore.BLUE}[7/7] Thêm dữ liệu lỗi{Style.RESET_ALL}")
    num_errors = num_records // 10  # 10% dữ liệu bị lỗi
    error_indices = random.sample(range(num_records), num_errors)

    for idx in error_indices:
        prices[idx] = np.nan

    print(f"→ Đã thêm {num_errors:,} lỗi (NaN) vào cột price")
    print(f"→ Tỷ lệ lỗi: {(num_errors/num_records)*100:.1f}%")
    return prices

def save_to_csv(data, student_id):
    """Lưu dữ liệu vào file CSV"""
    print(f"\n{Fore.YELLOW}Lưu dữ liệu vào CSV{Style.RESET_ALL}")

    # Tạo DataFrame và lưu vào thư mục output
    df = pd.DataFrame(data)
    output_file = os.path.join('output', f'transactions_{student_id}.csv')
    df.to_csv(output_file, index=False)

    print(f"→ Đã lưu vào file: {output_file}")
    print(f"→ Kích thước dữ liệu: {len(df):,} dòng × {len(df.columns)} cột")
    return df

def generate_data(student_id):
    print(f"\n{Fore.GREEN}Bắt đầu tạo dữ liệu...{Style.RESET_ALL}")
    print("=" * 50)

    num_records = 1_000_000
    print(f"Số lượng bản ghi cần tạo: {num_records:,}\n")

    # 1. Tạo tên sản phẩm
    product_names = create_product_names(num_records)

    # 2. Tạo customer IDs
    customer_ids = create_customer_ids(student_id, num_records)

    # 3. Tạo chuỗi thời gian
    order_dates = create_order_dates(num_records)

    # 4. Tạo giá sản phẩm
    prices = create_prices(num_records)

    # 5. Tạo số lượng
    quantities = create_quantities(num_records)

    # 6. Tạo giảm giá
    discounts = create_discounts(num_records)

    # 7. Thêm lỗi
    prices = add_errors(prices, num_records)

    # Tạo DataFrame và lưu file
    data = {
        'product_name': product_names,
        'customer_id': customer_ids,
        'order_date': order_dates,
        'price': prices,
        'quantity': quantities,
        'discount': discounts
    }

    df = save_to_csv(data, student_id)

    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Hoàn thành tạo dữ liệu!{Style.RESET_ALL}")

    return df

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        generate_data(student_id)
    else:
        print("Usage: python generate_data.py <student_id>")
