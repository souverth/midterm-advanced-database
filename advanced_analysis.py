import sys
import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import init, Fore, Style
import re

init()  # Khởi tạo colorama

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

os.environ["LOKY_MAX_CPU_COUNT"] = "4"
os.environ['JOBLIB_TEMP_FOLDER'] = os.path.expanduser('~')

def normalize_product_name(name):
    """UDF chuẩn hóa tên sản phẩm"""
    # Chuyển thành chữ thường
    name = str(name).lower()

    # Xóa ký tự đặc biệt, giữ lại chữ và số
    name = re.sub(r'[^a-z0-9\s]', '', name)

    # Xóa khoảng trắng thừa
    name = ' '.join(name.split())

    return name

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

def create_daily_features(df):
    """Tạo đặc trưng theo ngày"""
    print(f"\n{Fore.BLUE}[2/4] Tạo đặc trưng theo ngày{Style.RESET_ALL}")

    # Thêm cột ngày
    df['date'] = df['order_date'].dt.date

    daily_features = pd.DataFrame()

    # 1. Tổng doanh thu
    daily_features['total_revenue'] = df.groupby('date')['total_amount'].sum()

    # 2. Số lượng đơn hàng
    daily_features['total_orders'] = df.groupby('date').size()

    # 3. Giá trị đơn hàng trung bình
    daily_features['avg_order_value'] = daily_features['total_revenue'] / daily_features['total_orders']

    # 4. Tổng số sản phẩm bán được
    daily_features['total_items'] = df.groupby('date')['quantity'].sum()

    # 5. Tỷ lệ giảm giá trung bình
    daily_features['avg_discount'] = df.groupby('date')['discount'].mean()

    print("\nThống kê đặc trưng theo ngày:")
    print(daily_features.describe().round(2).to_string())
    return daily_features

def cluster_daily_patterns(features, n_clusters=4):
    """Phân cụm mẫu hình ngày"""
    print(f"\n{Fore.BLUE}[3/4] Phân cụm mẫu hình ngày{Style.RESET_ALL}")

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Thực hiện phân cụm
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)

    # Thêm nhãn cụm vào DataFrame
    features['cluster'] = clusters

    # Thống kê về các cụm
    print("\nThống kê theo cụm:")
    for i in range(n_clusters):
        cluster_stats = features[features['cluster'] == i].mean()
        size = len(features[features['cluster'] == i])
        print(f"\nCụm {i} ({size} ngày):")
        print(f"→ Doanh thu trung bình/ngày: ${cluster_stats['total_revenue']:,.2f}")
        print(f"→ Số đơn hàng trung bình/ngày: {cluster_stats['total_orders']:.0f}")
        print(f"→ Giá trị đơn hàng trung bình: ${cluster_stats['avg_order_value']:.2f}")
        print(f"→ Số sản phẩm trung bình/ngày: {cluster_stats['total_items']:.0f}")
        print(f"→ Tỷ lệ giảm giá trung bình: {cluster_stats['avg_discount']:.2%}")

    return features, features_scaled

def visualize_clusters(features, features_scaled, student_id):
    """Tạo biểu đồ phân cụm"""
    print(f"\n{Fore.BLUE}[4/4] Tạo biểu đồ phân cụm{Style.RESET_ALL}")

    # 1. Biểu đồ phân tán (Scatter plot)
    plt.figure(figsize=(15, 5), facecolor='white')

    # PCA để giảm chiều dữ liệu xuống 2D
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    features_pca = pca.fit_transform(features_scaled)

    # Biểu đồ phân cụm
    plt.subplot(1, 3, 1)
    scatter = plt.scatter(features_pca[:, 0], features_pca[:, 1],
                         c=features['cluster'], cmap='viridis')
    plt.title('Phân cụm mẫu hình ngày (PCA)')
    plt.xlabel('Thành phần chính 1')
    plt.ylabel('Thành phần chính 2')
    plt.colorbar(scatter)

    # 2. Biểu đồ phân phối doanh thu theo cụm
    plt.subplot(1, 3, 2)
    sns.boxplot(x='cluster', y='total_revenue', data=features)
    plt.title('Phân phối doanh thu theo cụm')
    plt.xlabel('Cụm')
    plt.ylabel('Doanh thu ($)')

    # 3. Biểu đồ số lượng đơn theo cụm
    plt.subplot(1, 3, 3)
    sns.boxplot(x='cluster', y='total_orders', data=features)
    plt.title('Phân phối số đơn theo cụm')
    plt.xlabel('Cụm')
    plt.ylabel('Số đơn hàng')

    plt.tight_layout()

    # Lưu biểu đồ vào thư mục img
    output_file = os.path.join('img', f'daily_patterns_clusters_{student_id}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"→ Đã lưu biểu đồ vào file: {output_file}")

    # Lưu kết quả phân cụm
    output_csv = os.path.join('output', f'daily_patterns_{student_id}.csv')
    features.to_csv(output_csv)
    print(f"→ Đã lưu kết quả phân cụm vào file: {output_csv}")

def analyze_advanced(student_id=None):
    print(f"\n{Fore.GREEN}Bắt đầu phân tích nâng cao...{Style.RESET_ALL}")
    print("=" * 50)

    # Nếu không có student_id, hiển thị danh sách file để chọn
    if student_id is None:
        student_id = list_available_files()
        if student_id is None:
            return None

    # 1. Đọc dữ liệu
    df = load_data(student_id)

    # 2. Tạo đặc trưng theo ngày
    features = create_daily_features(df)

    # 3. Phân cụm
    features, features_scaled = cluster_daily_patterns(features)

    # 4. Tạo biểu đồ
    visualize_clusters(features, features_scaled, student_id)

    print("\n" + "=" * 50)
    print(f"{Fore.GREEN}Hoàn thành phân tích nâng cao!{Style.RESET_ALL}")

    return features

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        analyze_advanced(student_id)
    else:
        print("Usage: python advanced_analysis.py <student_id>")
