import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import threading

# Khai báo biến driver ở mức độ toàn cục
driver = None

def open_facebook_with_cookie(cookie, user_agent=None):
    global driver  # Sử dụng biến driver toàn cục

    try:
        # Thiết lập tùy chọn của Chrome
        chrome_options = Options()

        # Thiết lập User-Agent nếu được cung cấp
        if user_agent:
            chrome_options.add_argument(f'user-agent={user_agent}')

        # Mở trình duyệt Chrome với tùy chọn đã thiết lập
        driver = webdriver.Chrome(options=chrome_options)

        # Mở trang web https://mbasic.facebook.com
        driver.get("https://www.facebook.com/")

        # Thực hiện đăng nhập bằng cookie
        try:
            # Tách cookie thành các cặp tên và giá trị
            cookie_pairs = cookie.strip().split(';')
            cookies = {}
            for pair in cookie_pairs:
                name, value = pair.strip().split('=')
                cookies[name] = value
            # Thêm từng cookie vào trình duyệt
            for name, value in cookies.items():
                driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com'})
        except Exception as e:
            messagebox.showerror("Error", "Invalid cookie format.")
            driver.quit()
            return

        # Refresh trang để áp dụng cookie
        driver.refresh()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        if driver is not None:
            driver.quit()
        print("Selenium error:", e)  # In ra thông điệp lỗi từ Selenium

def run_facebook_with_cookie():
    global driver  # Sử dụng biến driver toàn cục
    try:
        # Lấy cookie từ ô nhập
        cookie = cookie_entry.get().strip()

        # Lấy User-Agent từ ô nhập
        user_agent = useragent_entry.get().strip()

        # Nếu có một trình duyệt đang chạy, đóng nó trước
        if driver is not None:
            driver.quit()
        
        # Mở trang Facebook với cookie và User-Agent (nếu có) và chờ trong một luồng mới
        threading.Thread(target=open_facebook_with_cookie, args=(cookie, user_agent)).start()
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    # Tạo cửa sổ tkinter và đặt kích thước
    root = tk.Tk()
    root.title("Login to Facebook with Cookie")
    root.geometry("400x200")

    # Tạo một nhãn chú thích cho ô nhập Cookie
    cookie_label = tk.Label(root, text="Nhập cookie:")
    cookie_label.pack(pady=5)

    # Tạo một ô nhập Cookie
    cookie_entry = tk.Entry(root, width=60)
    cookie_entry.pack(pady=5)

    # Tạo một nhãn chú thích cho ô nhập User-Agent
    useragent_label = tk.Label(root, text="Nhập User-Agent (nếu không có sẽ tự động fake):")
    useragent_label.pack(pady=5)

    # Tạo một ô nhập User-Agent
    useragent_entry = tk.Entry(root, width=60)
    useragent_entry.pack(pady=5)

    # Tạo một nút để đăng nhập vào Facebook với Cookie và User-Agent
    login_button = tk.Button(root, text="Đăng nhập", command=run_facebook_with_cookie)
    login_button.pack(pady=5)

    # Hiển thị cửa sổ
    root.mainloop()
