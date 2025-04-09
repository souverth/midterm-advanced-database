import sys
import os
import platform
import subprocess

# Tạo thư mục output và img nếu chưa tồn tại
os.makedirs('output', exist_ok=True)
os.makedirs('img', exist_ok=True)

def clear_screen():
    """Xóa terminal trên cả Windows và Unix"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def install_requirements():
    """Kiểm tra và cài đặt các thư viện cần thiết"""
    from colorama import init, Fore, Style
    init()

    requirements = [
        'pandas',
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'colorama'
    ]

    print(f"\n{Fore.BLUE}Kiểm tra thư viện...{Style.RESET_ALL}")
    for package in requirements:
        try:
            __import__(package)
            print(f"{Fore.GREEN}✓ {package}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.YELLOW}→ Cài đặt {package}...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            print(f"{Fore.GREEN}✓ Đã cài đặt {package}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}✓ Đã cài đặt đầy đủ thư viện!{Style.RESET_ALL}")

def print_menu():
    """Hiển thị menu chức năng"""
    from colorama import init, Fore, Style
    init()

    print("\n" + Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "PHÂN TÍCH DỮ LIỆU GIAO DỊCH" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(f"{Fore.CYAN}1. Sinh dữ liệu cá nhân hóa (10 điểm){Style.RESET_ALL}")
    print(f"{Fore.CYAN}2. Tiền xử lý dữ liệu(20 điểm){Style.RESET_ALL}")
    print(f"{Fore.CYAN}3. Phân tích dữ liệu (30 điểm){Style.RESET_ALL}")
    print(f"{Fore.CYAN}4. Phát hiện giao dịch bất thường (20 điểm){Style.RESET_ALL}")
    print(f"{Fore.CYAN}5. Tùy chọn nâng cao (20 điểm bonus){Style.RESET_ALL}")
    print(f"{Fore.RED}6. Thoát{Style.RESET_ALL}")
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def main():
    """Chương trình chính"""
    from colorama import init, Fore, Style
    init()

    clear_screen()
    print(f"{Fore.GREEN}Khởi tạo chương trình...{Style.RESET_ALL}")
    install_requirements()

    # Import các module sau khi đã cài đặt thư viện
    from genarate_data import generate_data
    from process_data import process_data
    from analyze_data import analyze_data
    from detect_anomalies import detect_anomalies
    from advanced_analysis import analyze_advanced

    while True:
        clear_screen()
        print_menu()

        choice = input(f"\n{Fore.YELLOW}Nhập lựa chọn của bạn (1-6): {Style.RESET_ALL}")

        if choice == "6":
            print(f"\n{Fore.GREEN}Cảm ơn bạn đã sử dụng chương trình!{Style.RESET_ALL}")
            break

        try:
            if choice == "1":
                student_id = input(f"{Fore.YELLOW}Nhập mã sinh viên: {Style.RESET_ALL}")
                clear_screen()
                print(f"\n{Fore.GREEN}TẠO DỮ LIỆU MẪU{Style.RESET_ALL}")
                print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                generate_data(student_id)

            elif choice == "2":
                clear_screen()
                print(f"\n{Fore.GREEN}Tiền xử lý dữ liệu{Style.RESET_ALL}")
                print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                process_data()
            elif choice == "3":
                clear_screen()
                print(f"\n{Fore.GREEN}PHÂN TÍCH DỮ LIỆU{Style.RESET_ALL}")
                print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                analyze_data()
            elif choice == "4":
                clear_screen()
                print(f"\n{Fore.GREEN}PHÁT HIỆN GIAO DỊCH BẤT THƯỜNG{Style.RESET_ALL}")
                print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                detect_anomalies()

            elif choice == "5":
                clear_screen()
                print(f"\n{Fore.GREEN}PHÂN TÍCH NÂNG CAO{Style.RESET_ALL}")
                print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                analyze_advanced()

            else:
                print(f"\n{Fore.RED}Lựa chọn không hợp lệ!{Style.RESET_ALL}")

        except Exception as e:
            print(f"\n{Fore.RED}Lỗi: {str(e)}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Nhấn Enter để tiếp tục...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã dừng chương trình.")
    except Exception as e:
        print(f"\nLỗi không mong muốn: {str(e)}")
