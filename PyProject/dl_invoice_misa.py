from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

import time
import os

# --- Cấu hình chung ---
MEINVOICE_URL = "https://www.meinvoice.vn/tra-cuu/"
CHROMEDRIVER_PATH = "chromedriver.exe" # Đảm bảo file này nằm cùng thư mục với script
DOWNLOAD_DIR = "D:\\PythonInvoiceMisa" # Thư mục để lưu hóa đơn đã tải
INVOICE_CODES_FILE = "invoice_codes.txt" # Tên file chứa mã hóa đơn
WAIT_TIMEOUT = 15 # Thời gian chờ tối đa cho các hành động quan trọng (giây)
SHORT_WAIT = 2    # Thời gian chờ ngắn giữa các bước (giây)

# 1. Hàm mở trình duyệt và cấu hình tải xuống
def open_browser():
    """
    Khởi tạo và cấu hình trình duyệt Chrome.
    Cấu hình thư mục mặc định để tải xuống.
    """
    # Đảm bảo thư mục download tồn tại
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Đã tạo thư mục tải xuống: {DOWNLOAD_DIR}")

    chrome_options = Options()
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False, # Không hỏi khi tải xuống
        "download.directory_upgrade": True,
        "safeBrowse.enabled": True,
        "plugins.always_open_pdf_externally": True # Mở PDF bên ngoài trình duyệt
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless") # Bỏ comment nếu muốn chạy ẩn danh
    chrome_options.add_argument("--start-maximized") # Phóng to cửa sổ trình duyệt

    try:
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Trình duyệt đã được mở và cấu hình.")
        return driver
    except WebDriverException as e:
        print(f"Lỗi khi mở trình duyệt: {e}")
        print("Hãy đảm bảo 'chromedriver.exe' đúng phiên bản và nằm trong cùng thư mục.")
        return None

# 2. Hàm nhập mã tra cứu hóa đơn
def enter_code(driver, invoice_code):
    """
    Nhập mã hóa đơn vào trường 'Mã tra cứu'.
    Sử dụng ID 'txtCode' để định vị.
    """
    try:
        input_invoice_code = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "txtCode"))
        )
        input_invoice_code.clear()
        input_invoice_code.send_keys(invoice_code)
        print(f"Đã nhập mã tra cứu: '{invoice_code}'.")
        return True
    except TimeoutException:
        print(f"Lỗi: Không tìm thấy trường nhập mã tra cứu sau {WAIT_TIMEOUT} giây.")
        return False
    except Exception as e:
        print(f"Lỗi khi nhập mã tra cứu: {e}")
        return False

# 3. Hàm thực hiện tìm kiếm
def click_search(driver):
    """
    Nhấp vào nút 'Tìm kiếm'.
    Sử dụng ID 'btnSearchInvoice' để định vị.
    Sẽ chờ nút có thể nhấp được.
    """
    try:
        search_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "btnSearchInvoice"))
        )
        search_button.click()
        print("Đã nhấp nút 'Tìm kiếm'.")
        time.sleep(SHORT_WAIT) # Thêm một chút thời gian chờ sau khi click
        return True
    except TimeoutException:
        print(f"Lỗi: Không tìm thấy hoặc không nhấp được nút 'Tìm kiếm' sau {WAIT_TIMEOUT} giây. Thử click bằng JavaScript.")
        try:
            search_button_js = WebDriverWait(driver, SHORT_WAIT).until(
                EC.presence_of_element_located((By.ID, "btnSearchInvoice"))
            )
            driver.execute_script("arguments[0].click();", search_button_js)
            print("Đã nhấp nút 'Tìm kiếm' bằng JavaScript.")
            time.sleep(SHORT_WAIT) # Thêm một chút thời gian chờ sau khi click bằng JS
            return True
        except TimeoutException:
            print("Lỗi: Không thể tìm thấy nút 'Tìm kiếm' ngay cả với JavaScript click.")
            return False
        except Exception as e_js:
            print(f"Lỗi khi nhấp nút tìm kiếm bằng JavaScript: {e_js}")
            return False
    except Exception as e:
        print(f"Lỗi khi nhấp nút tìm kiếm: {e}")
        return False

# 4. Hàm kiểm tra kết quả tìm kiếm
def check_result(driver):
    """
    Kiểm tra kết quả tìm kiếm hóa đơn.
    Trả về True nếu tìm thấy hóa đơn, False nếu không tìm thấy (popup lỗi).
    """
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Tải hóa đơn')]")),
                EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']//*[contains(text(),'Không tìm thấy hóa đơn')]"))
            )
        )

        try:
            error_message_in_modal = driver.find_element(By.XPATH, "//div[@class='modal-content']//*[contains(text(),'Không tìm thấy hóa đơn')]")
            if error_message_in_modal.is_displayed():
                print("Kết quả: Không tìm thấy hóa đơn (popup lỗi).")
                try:
                    retry_button = WebDriverWait(driver, SHORT_WAIT).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-content']//button[contains(.,'Nhập lại mã tra cứu')]"))
                    )
                    retry_button.click()
                    print("Đã đóng popup lỗi.")
                except TimeoutException:
                    try:
                        close_button_x = WebDriverWait(driver, SHORT_WAIT).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-header']/button[@class='close']"))
                        )
                        close_button_x.click()
                        print("Đã đóng popup lỗi bằng nút 'X'.")
                    except Exception as e_close:
                        print(f"Cảnh báo: Không thể đóng popup lỗi: {e_close}")
                time.sleep(SHORT_WAIT)
                return False
        except NoSuchElementException:
            pass

        try:
            download_button = driver.find_element(By.XPATH, "//button[contains(.,'Tải hóa đơn')]")
            if download_button.is_displayed():
                return True
        except NoSuchElementException:
            pass

        print("Kết quả: Không xác định. Trang không hiển thị nút tải hoặc popup lỗi.")
        return False

    except TimeoutException:
        print(f"Lỗi: Không nhận được kết quả tìm kiếm (hoặc popup lỗi) sau {WAIT_TIMEOUT} giây.")
        return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra kết quả: {e}")
        return False

# 5. Hàm tải hóa đơn
def download_invoice(driver):
    """
    Tải hóa đơn điện tử dạng XML (và PDF nếu cần).
    """
    try:
        download_main_button = WebDriverWait(driver, SHORT_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Tải hóa đơn')]"))
        )
        download_main_button.click()
        print("Đã nhấp nút 'Tải hóa đơn'.")
        time.sleep(SHORT_WAIT)

        xml_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "txt-download-xml"))
        )
        driver.execute_script("arguments[0].click();", xml_button)
        print("Đã tải hóa đơn dạng XML.")
        time.sleep(SHORT_WAIT)

        # pdf_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "txt-download-pdf"))
        # )
        # driver.execute_script("arguments[0].click();", pdf_button)
        # print("Đã tải hóa đơn dạng PDF.")
        # time.sleep(SHORT_WAIT)

        return True
    except TimeoutException:
        print(f"Lỗi: Không tìm thấy nút tải XML sau {WAIT_TIMEOUT} giây.")
        return False
    except Exception as e:
        print(f"Lỗi khi tải hóa đơn: {e}")
        return False

# Hàm đọc mã hóa đơn từ file TXT
def read_invoice_codes_from_txt(file_path):
    """
    Đọc danh sách mã hóa đơn từ một file .txt, mỗi mã trên một dòng.
    Bỏ qua các dòng trống.
    """
    invoice_codes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                code = line.strip()
                if code:
                    invoice_codes.append(code)
        print(f"Đã đọc {len(invoice_codes)} mã hóa đơn từ '{file_path}'.")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file mã hóa đơn '{file_path}'.")
    except Exception as e:
        print(f"Lỗi khi đọc file mã hóa đơn: {e}")
    return invoice_codes

# Hàm chính để điều phối
def main():
    """
    Chức năng chính của chương trình. Đọc mã hóa đơn từ file TXT và thực hiện tra cứu/tải xuống.
    """
    invoice_codes = read_invoice_codes_from_txt(INVOICE_CODES_FILE)
    if not invoice_codes:
        print("Không có mã hóa đơn nào để xử lý. Chương trình kết thúc.")
        return

    driver = open_browser()
    if driver is None:
        return

    for index, code in enumerate(invoice_codes):
        print(f"\n--- Xử lý mã hóa đơn ({index+1}/{len(invoice_codes)}) ---") # Đã loại bỏ code khỏi dòng này

        driver.get(MEINVOICE_URL)
        
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "txtCode"))
            )
        except TimeoutException:
            print(f"Lỗi: Không thể tải trang tra cứu hoặc tìm thấy trường nhập mã. Bỏ qua.") # Đã loại bỏ code
            continue

        if not enter_code(driver, code):
            continue

        if not click_search(driver):
            continue

        if check_result(driver):
            print(f"Mã tra cứu: Tìm thấy hóa đơn. Đang tiến hành tải xuống...") # Đã thay thế '{code}' bằng 'Mã tra cứu'
            download_invoice(driver)
        else:
            print(f"Mã tra cứu: Không tìm thấy hóa đơn hoặc có lỗi. Đã xử lý popup (nếu có).") # Đã thay thế '{code}' bằng 'Mã tra cứu'
            
        time.sleep(SHORT_WAIT)

    print("\nQuá trình hoàn tất. Đang đóng trình duyệt...")
    driver.quit()
    print("Trình duyệt đã đóng.")

if __name__ == "__main__":
    main()
# def main():
#     # - Truy cập trang web tra cứu hóa đơn điện tử của meinvoice.vn
#     # 1. Hàm mở trình duyệt: cấu hình dowload file selenium

#     # -Nhập mã tra cứu hóa đơn vào trường tương ứng
#     # 2. Hàm nhập mã tra cứu

#     # - Thực hiện hành động tìm tiếm
#     # 3. Hàm thực hiện tìm kiếm

#     # - Xử lý kết quả tìm kiếm, bao gồm việc nhận diện hóa đơn và tùy chọn tải xuống
#     # 4. Hàm xử lý kết quả: thành công hoặc thất bại if else

#     # - Tải hóa đơn điện tử (dạng PDF) về hệ thống cục bộ
#     # 5. Tải hóa đơn: tra cứu thành công

#     print()