from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import openpyxl 
import os
import time
import xml.etree.ElementTree as ET


# Thư mục chứa tệp input và nơi tải xuống hóa đơn
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(CURRENT_DIR, "input.xlsx")
OUTPUT_FILE = os.path.join(CURRENT_DIR, "output.xlsx")
DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "downloaded_invoices")

# Tạo thư mục tải xuống nếu chưa có
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Khởi tạo driver (sẽ được gán trong hàm main)
driver = None

# --- Các hàm xử lý ---

def handle_input():
    """Đọc file input.xlsx"""
    try:
        return pd.read_excel(INPUT_FILE)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file input.xlsx tại {INPUT_FILE}")
        return pd.DataFrame() # Trả về DataFrame rỗng nếu không tìm thấy

def open_browser(path_download):
    """Mở Chrome với các tùy chọn tải xuống"""
    global driver # Khai báo để có thể gán driver toàn cục
    chrome_options = Options()

    prefs = {
        "download.default_directory": path_download,
        "download.prompt_for_download": False, # Không hỏi khi tải xuống
        "download.directory_upgrade": True,
        "disable-popup-blocking": True,
        "safeBrowse.enabled": True,
        "plugins.always_open_pdf_externally": True # Tải PDF thay vì mở trong trình duyệt
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # 

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10) # Đặt thời gian chờ ngầm định
    return driver

def check_load_success(current_driver, invoice_type):
    """
    Kiểm tra xem trang đã tải hóa đơn thành công hay chưa.
    Tùy chỉnh logic kiểm tra cho từng loại hóa đơn.
    """
    if invoice_type == "fpt":
        try:
            # Chờ thông tin chi tiết hóa đơn xuất hiện
            WebDriverWait(current_driver, 15).until(
                EC.presence_of_element_located((By.ID, "invoiceDetail"))
            )
            return True
        except TimeoutException:
            return False
    elif invoice_type == "meinvoice":
        # Cần định nghĩa XPath/CSS selector cho trường hợp Misa
        try:
            
            WebDriverWait(current_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Thông tin hóa đơn')]")) # XPath giả định
            )
            return True
        except TimeoutException:
            return False
    elif invoice_type == "van.ehoadon":
        try:
            # Chờ iframe chứa hóa đơn xuất hiện
            WebDriverWait(current_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="frameViewInvoice"]'))
            )
            return True
        except TimeoutException:
            return False
    return False

def check_load_fail(current_driver, invoice_type):
    """
    Kiểm tra xem có thông báo lỗi tải hóa đơn hay không.
    Tùy chỉnh logic kiểm tra cho từng loại hóa đơn.
    """
    if invoice_type == "fpt":
        try:
            # Chờ thông báo lỗi (toast-message) xuất hiện
            WebDriverWait(current_driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "toast-message"))
            )
            return True
        except TimeoutException:
            return False
    elif invoice_type == "meinvoice":
        # Cần định nghĩa XPath/CSS selector cho trường hợp lỗi Misa
        try:
            # 
            WebDriverWait(current_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Không tìm thấy hóa đơn')]")) # XPath giả định
            )
            return True
        except TimeoutException:
            return False
    elif invoice_type == "van.ehoadon":
        # Đối với van.ehoadon, việc không tìm thấy iframe có thể được coi là lỗi
        # Hoặc tìm một thông báo lỗi cụ thể nếu có
        try:
            # 
            WebDriverWait(current_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Không tìm thấy dữ liệu')]")) # XPath giả định
            )
            return True
        except TimeoutException:
            return False
    return False

def handle_download_file(current_driver, invoice_type):
    """
    Xử lý việc tải file hóa đơn (PDF/XML).
    Trả về tên file XML nếu tải thành công, None nếu chỉ tải PDF hoặc lỗi.
    """
    downloaded_file_name = None
    if invoice_type == "fpt":
        try:
            # Ưu tiên tải XML
            download_xml_button = WebDriverWait(current_driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn') and contains(text(), 'Tải XML')]"))
            )
            download_xml_button.click()
            print("Đang tải hóa đơn XML từ FPT...")
            time.sleep(3) # Chờ tệp tải xuống

            
            downloaded_files = [f for f f in os.listdir(DOWNLOAD_DIR) if f.endswith('.xml')]
            if downloaded_files:
                downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
                downloaded_file_name = downloaded_files[0]
                print(f"Đã tải thành công file XML: {downloaded_file_name}")
            else:
                print("Không tìm thấy tệp XML đã tải xuống.")

        except TimeoutException:
            print("Không tìm thấy nút 'Tải XML'. Thử tìm 'Tải PDF'.")
            try:
                download_pdf_button = WebDriverWait(current_driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn') and contains(text(), 'Tải PDF')]"))
                )
                download_pdf_button.click()
                print("Đang tải hóa đơn PDF từ FPT...")
                time.sleep(3) # Chờ PDF tải xuống
                downloaded_file_name = "PDF_Downloaded" # Đánh dấu là đã tải PDF
            except TimeoutException:
                print("Không tìm thấy nút 'Tải PDF' hoặc 'Tải XML'.")
    elif invoice_type == "meinvoice":
        
        try:
            # Tìm và click nút tải XML
            download_xml_button = WebDriverWait(current_driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnDownloadXml")) # Thay bằng ID/XPath thực tế của Misa
            )
            download_xml_button.click()
            print("Đang tải hóa đơn XML từ Misa...")
            time.sleep(3) # 
            downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.xml')]
            if downloaded_files:
                downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
                downloaded_file_name = downloaded_files[0]
                print(f"Đã tải thành công file XML: {downloaded_file_name}")
            else:
                print("Không tìm thấy tệp XML đã tải xuống.")
        except TimeoutException:
            print("Không tìm thấy nút 'Tải XML' trên Misa.")
    elif invoice_type == "van.ehoadon":
        try:
            # Chuyển sang iframe trước khi tìm nút download
            xpath_frame = '//*[@id="frameViewInvoice"]'
            WebDriverWait(current_driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_frame)))
            element_frame = current_driver.find_element(By.XPATH, xpath_frame)
            current_driver.switch_to.frame(element_frame)

            # download PDF 
            print("Đang tải PDF từ Van.eHoadon...")
            element_download = WebDriverWait(current_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="btnDownload"]')) # Hoặc các ID/XPath khác
            )
            try:
                element_download.click()
            except: # 
                current_driver.execute_script("arguments[0].click()", element_download)
            time.sleep(2) # 

            # download XML
            print("Đang tải XML từ Van.eHoadon...")
            css_download_xml = '#LinkDownXML' # 
            element_download_xml = WebDriverWait(current_driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_download_xml))
            )
            try:
                element_download_xml.click()
            except: # 
                current_driver.execute_script("arguments[0].click()", element_download_xml)
            time.sleep(3) # 

            # 
            downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.xml')]
            if downloaded_files:
                downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)
                downloaded_file_name = downloaded_files[0]
                print(f"Đã tải thành công file XML: {downloaded_file_name}")
            else:
                print("Không tìm thấy tệp XML đã tải xuống.")

            current_driver.switch_to.default_content() # Quay lại frame chính
        except TimeoutException:
            print("Không tìm thấy các nút tải xuống hoặc iframe trên Van.eHoadon.")
        except Exception as e:
            print(f"Lỗi khi tải hóa đơn Van.eHoadon: {e}")
            current_driver.switch_to.default_content() # Đảm bảo quay lại frame chính

    return downloaded_file_name

def extract_xml_data(xml_file_path):
    """
    Trích xuất thông tin từ tệp XML hóa đơn.
    Cần điều chỉnh XPath tùy theo cấu trúc XML của từng nhà cung cấp.
    """
    data = {
        "SoHoaDon": "",
        "DonViBanHang": "",
        "MaSoThueBan": "",
        "DiaChiBan": "",
        "SoTaiKhoanBan": "",
        "HoTenNguoiMuaHang": "",
        "DiaChiMua": "",
        "MaSoThueMua": ""
    }
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        
        data["SoHoaDon"] = root.findtext(".//InvoiceNo") or root.findtext(".//InvoiceHeader/InvoiceNo") or ""

        
        seller_node = root.find(".//SellerInfo") or root.find(".//InvoiceHeader/Seller")
        if seller_node is not None:
            data["DonViBanHang"] = seller_node.findtext(".//SellerLegalName") or seller_node.findtext(".//Name") or ""
            data["MaSoThueBan"] = seller_node.findtext(".//SellerTaxCode") or seller_node.findtext(".//TaxCode") or ""
            data["DiaChiBan"] = seller_node.findtext(".//SellerAddress") or seller_node.findtext(".//Address") or ""
            data["SoTaiKhoanBan"] = seller_node.findtext(".//SellerBankAccount") or seller_node.findtext(".//BankAccount") or ""

       
        buyer_node = root.find(".//BuyerInfo") or root.find(".//InvoiceHeader/Buyer")
        if buyer_node is not None:
            data["HoTenNguoiMuaHang"] = buyer_node.findtext(".//BuyerLegalName") or buyer_node.findtext(".//Name") or ""
            data["DiaChiMua"] = buyer_node.findtext(".//BuyerAddress") or buyer_node.findtext(".//Address") or ""
            data["MaSoThueMua"] = buyer_node.findtext(".//BuyerTaxCode") or buyer_node.findtext(".//TaxCode") or ""

    except Exception as e:
        print(f"Lỗi khi đọc file XML {xml_file_path}: {e}")
    return data

def process_fpt_invoice(current_driver, url, ma_so_thue, ma_tra_cuu):
    """Xử lý loại hóa đơn FPT"""
    current_driver.get(url)
    try:
        xpath_ma_so_thue = "//input[@placeholder='MST bên bán']" # Đã sửa lỗi chính tả
        mst_input = WebDriverWait(current_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ma_so_thue))
        )
        mst_input.send_keys(ma_so_thue)
        time.sleep(1)

        xpath_ma_tra_cuu = "//input[@placeholder='Mã tra cứu hóa đơn']"
        lookup_input = WebDriverWait(current_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ma_tra_cuu))
        )
        lookup_input.send_keys(ma_tra_cuu)

        xpath_btn = '//div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button' # XPath nút "Tra cứu"
        search_button = WebDriverWait(current_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_btn))
        )
        search_button.click()

        print(f"Đang tra cứu FPT: MST={ma_so_thue}, Mã tra cứu={ma_tra_cuu}")
        # Check success
        if check_load_success(current_driver, "fpt"):
            print("Tra cứu FPT thành công.")
            downloaded_xml = handle_download_file(current_driver, "fpt")
            return "success", downloaded_xml
        # Check fail
        elif check_load_fail(current_driver, "fpt"):
            print("Tra cứu FPT thất bại: Không tìm thấy hóa đơn hoặc thông tin không hợp lệ.")
            return "fail", None
        else:
            print("Tra cứu FPT: Không xác định được trạng thái.")
            return "fail", None #
    except TimeoutException as e:
        print(f"Lỗi Timeout khi xử lý FPT invoice: {e}")
        return "fail", None
    except NoSuchElementException as e:
        print(f"Lỗi không tìm thấy phần tử khi xử lý FPT invoice: {e}")
        return "fail", None
    except Exception as e:
        print(f"Lỗi không xác định khi xử lý FPT invoice: {e}")
        return "fail", None

def process_me_invoice(current_driver, url, ma_so_thue, ma_tra_cuu):
    """Xử lý loại hóa đơn Misa"""
    current_driver.get(url)
    try:
       
        xpath_ma_so_thue = "//input[@id='txtMST']" # 
        mst_input = WebDriverWait(current_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ma_so_thue))
        )
        mst_input.send_keys(ma_so_thue)
        time.sleep(1)

        xpath_ma_tra_cuu = "//input[@id='txtMaTraCuu']" # 
        lookup_input = WebDriverWait(current_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ma_tra_cuu))
        )
        lookup_input.send_keys(ma_tra_cuu)

        xpath_btn = "//button[@id='btnSearchInvoice']" # 
        search_button = WebDriverWait(current_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_btn))
        )
        search_button.click()

        print(f"Đang tra cứu Misa: MST={ma_so_thue}, Mã tra cứu={ma_tra_cuu}")
        if check_load_success(current_driver, "meinvoice"):
            print("Tra cứu Misa thành công.")
            downloaded_xml = handle_download_file(current_driver, "meinvoice")
            return "success", downloaded_xml
        elif check_load_fail(current_driver, "meinvoice"):
            print("Tra cứu Misa thất bại.")
            return "fail", None
        else:
            print("Tra cứu Misa: Không xác định được trạng thái.")
            return "fail", None
    except TimeoutException as e:
        print(f"Lỗi Timeout khi xử lý Misa invoice: {e}")
        return "fail", None
    except NoSuchElementException as e:
        print(f"Lỗi không tìm thấy phần tử khi xử lý Misa invoice: {e}")
        return "fail", None
    except Exception as e:
        print(f"Lỗi không xác định khi xử lý Misa invoice: {e}")
        return "fail", None

def process_van_e_invoice(current_driver, url, ma_so_thue, ma_tra_cuu): # 
    """Xử lý loại hóa đơn ehoadon (Van.eHoadon)"""
    current_driver.get(url)
    try:
        
        xpath_ma_tra_cuu = "//input[@placeholder='Mã tra cứu hóa đơn']" # 
        lookup_input = WebDriverWait(current_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_ma_tra_cuu))
        )
        lookup_input.send_keys(ma_tra_cuu)

        # 
        xpath_btn = '//*[@id="Button1"]' #
        element_btn = WebDriverWait(current_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_btn))
        )
        try:
            element_btn.click()
        except Exception: # Dùng except chung để bắt cả lỗi click và script execution
            current_driver.execute_script("arguments[0].click()", element_btn)

        time.sleep(2) # Đợi trang load hoặc iframe xuất hiện

        print(f"Đang tra cứu Van.eHoadon: Mã tra cứu={ma_tra_cuu}")
        if check_load_success(current_driver, "van.ehoadon"):
            print("Tra cứu Van.eHoadon thành công.")
            downloaded_xml = handle_download_file(current_driver, "van.ehoadon")
            return "success", downloaded_xml
        elif check_load_fail(current_driver, "van.ehoadon"):
            print("Tra cứu Van.eHoadon thất bại.")
            return "fail", None
        else:
            print("Tra cứu Van.eHoadon: Không xác định được trạng thái.")
            return "fail", None
    except TimeoutException as e:
        print(f"Lỗi Timeout khi xử lý Van.eHoadon invoice: {e}")
        return "fail", None
    except NoSuchElementException as e:
        print(f"Lỗi không tìm thấy phần tử khi xử lý Van.eHoadon invoice: {e}")
        return "fail", None
    except Exception as e:
        print(f"Lỗi không xác định khi xử lý Van.eHoadon invoice: {e}")
        return "fail", None

def process_invoice(df_input):
    """Xử lý từng loại hóa đơn dựa trên URL"""
    # Chuẩn bị DataFrame cho output
    output_columns = [
        "Mã số thuế (Input)", "Mã tra cứu (Input)", "URL (Input)", "Status", "Tên file tải về",
        "Số hóa đơn", "Đơn vị bán hàng", "Mã số thuế bán", "Địa chỉ bán",
        "Số tài khoản bán", "Họ tên người mua hàng", "Địa chỉ mua", "Mã số thuế mua"
    ]
    df_output = pd.DataFrame(columns=output_columns)

    global driver # Sử dụng driver toàn cục
    driver = open_browser(DOWNLOAD_DIR) # Mở trình duyệt một lần duy nhất

    for index, row in df_input.iterrows():
        str_ma_so_thue = str(row["Mã số thuế"]).strip()
        str_ma_tra_cuu = str(row["Mã tra cứu"]).strip()
        str_url = str(row["URL"]).strip().lower() # Chuyển về chữ thường để so sánh dễ hơn

        print(f"\n--- Đang xử lý: URL={str_url}, MST={str_ma_so_thue}, Mã tra cứu={str_ma_tra_cuu} ---")

        status = "fail"
        downloaded_xml_filename = None
        extracted_data = {}

        # ham tra cuu
        # chia thanh tung truong hop theo tung loai: misa, fpt, van
        if "fpt" in str_url:
            status, downloaded_xml_filename = process_fpt_invoice(driver, str_url, str_ma_so_thue, str_ma_tra_cuu)
        elif "meinvoice" in str_url:
            status, downloaded_xml_filename = process_me_invoice(driver, str_url, str_ma_so_thue, str_ma_tra_cuu)
        elif "van.ehoadon" in str_url:
            status, downloaded_xml_filename = process_van_e_invoice(driver, str_url, str_ma_so_thue, str_ma_tra_cuu)
        else:
            print(f"URL không được hỗ trợ: {str_url}")

        #Ham check ket qua
        #chia thanh tung truong hop theo tung loai: misa, fpt, van
        # success
        # fail
        if status == "success" and downloaded_xml_filename and downloaded_xml_filename != "PDF_Downloaded":
            # Ham doc du lieu
            #doc file
            xml_file_path = os.path.join(DOWNLOAD_DIR, downloaded_xml_filename)
            if os.path.exists(xml_file_path):
                # ham trich xuat du lieu
                # chia thanh tung truong hop theo tung loai: misa, fpt, van
                extracted_data = extract_xml_data(xml_file_path)
            else:
                print(f"Cảnh báo: Tệp XML '{downloaded_xml_filename}' không tồn tại sau khi tải.")
                status = "fail" # Đặt lại trạng thái nếu file không tồn tại
        elif status == "success" and downloaded_xml_filename == "PDF_Downloaded":
            print("Chỉ tải được PDF, không thể trích xuất dữ liệu.")


        row_output = {
            "Mã số thuế (Input)": str_ma_so_thue,
            "Mã tra cứu (Input)": str_ma_tra_cuu,
            "URL (Input)": str_url,
            "Status": status,
            "Tên file tải về": downloaded_xml_filename if downloaded_xml_filename else "",
            "SoHoaDon": extracted_data.get("SoHoaDon", ""),
            "DonViBanHang": extracted_data.get("DonViBanHang", ""),
            "MaSoThueBan": extracted_data.get("MaSoThueBan", ""),
            "DiaChiBan": extracted_data.get("DiaChiBan", ""),
            "SoTaiKhoanBan": extracted_data.get("SoTaiKhoanBan", ""),
            "HoTenNguoiMuaHang": extracted_data.get("HoTenNguoiMuaHang", ""),
            "DiaChiMua": extracted_data.get("DiaChiMua", ""),
            "MaSoThueMua": extracted_data.get("MaSoThueMua", "")
        }
        df_output = pd.concat([df_output, pd.DataFrame([row_output])], ignore_index=True)

    driver.quit() # 
    return df_output

def main():
    # 1. read input excel
    df = handle_input()

    if not df.empty:
        # 2. Process invoices
        df_output = process_invoice(df)

        # 3. Save output
        try:
            df_output.to_excel(OUTPUT_FILE, index=False)
            print(f"\nĐã hoàn tất. Kết quả được lưu vào: {OUTPUT_FILE}")
        except Exception as e:
            print(f"Lỗi khi lưu file output.xlsx: {e}")
    else:
        print("Không có dữ liệu trong file input.xlsx để xử lý.")

if __name__ == "__main__":
    main()