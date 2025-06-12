from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")

time.sleep(5)

all_pages_data = {}
page_number = 1

while True:
    print(f"Đang thu thập trang {page_number}...")

    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, ".list-tax-result .list-tax-row")
    page_data = []

    for row in rows:
        try:
            name = row.find_element(By.CLASS_NAME, "company-name").text
            mst = row.find_element(By.CLASS_NAME, "company-taxcode").text
            date = row.find_element(By.CLASS_NAME, "company-date").text
            page_data.append({
                "Tên doanh nghiệp": name,
                "Mã số thuế": mst,
                "Ngày cấp": date
            })
        except:
            continue

    all_pages_data[f"Trang {page_number}"] = pd.DataFrame(page_data)

    # Kiểm tra nút "Trang sau"
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(@class, 'next-page') and not(contains(@class,'disabled'))]")
        next_btn.click()
        page_number += 1
    except:
        break

driver.quit()

# Lưu từng trang vào từng sheet Excel
with pd.ExcelWriter("masothue.xlsx") as writer:
    for sheet_name, df in all_pages_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)