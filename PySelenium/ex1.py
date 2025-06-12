import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()

try:
    # 1. Mở trang web
    driver.get("https://www.saucedemo.com/")
    print(f"Đã mở trang: {driver.title}")

    # 2. Tìm ô username và nhập dữ liệu (Sửa ID từ 'user_name' thành 'user-name')
    username_input_id = 'user-name' 
    username_element = driver.find_element(By.ID, username_input_id)
    username_value = 'standard_user'
    username_element.send_keys(username_value)
    print(f"Đã nhập username: {username_value}")

    # 3. Tìm ô password và nhập dữ liệu
    password_input_id = 'password'
    password_element = driver.find_element(By.ID, password_input_id)
    password_value = 'secret_sauce'
    password_element.send_keys(password_value)
    print("Đã nhập password.")

    # 4. Tìm nút Login và nhấn vào nó
    login_button_id = 'login-button'
    login_button_element = driver.find_element(By.ID, login_button_id)
    login_button_element.click()
    print("Đã nhấn nút Login.")

    # Chờ một chút để trang mới tải xong
    time.sleep(2)

    # 5. Kiểm tra xem đã đăng nhập thành công chưa
    # Nếu thành công, URL sẽ chứa 'inventory.html' và tiêu đề trang là 'Swag Labs'
    if "inventory.html" in driver.current_url:
        print(f"Đăng nhập thành công! Tiêu đề trang mới là: {driver.title}")
    else:
        # Nếu có lỗi, tìm và in ra thông báo lỗi trên trang
        try:
            error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
            print(f"Đăng nhập thất bại. Lỗi: {error_message}")
        except:
            print("Đăng nhập thất bại và không tìm thấy thông báo lỗi cụ thể.")

finally:
    # 6. Đóng trình duyệt sau khi hoàn thành
    # Thêm một khoảng chờ ngắn để bạn có thể xem kết quả trước khi trình duyệt đóng
    time.sleep(3) 
    driver.quit()
    print("Đã đóng trình duyệt.")