from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract

def open_chorme():
    driver = webdriver.Chrome()
    driver.get()
    return driver

def xu_ly_bien_kiem_soat(driver):
    xpath_input = '//input[@id="formBSX"]/div[2]/div[1]/input'
    element = driver.find_element(By.XPATH, xpath_input)
    str_bien_so = "43D146872"
    element_input.send_keys(str_bien_so)    
    print()

def xu_ly_loai_phuong_tien(driver):
    """Xu ly chon loai phuong tien"""
    # click vao option loai phuong tien
    xpath_option = '//input[@id="formBSX"]/div[2]/div[2/select'
    element_input = driver.find_element(By.XPATH, xpath_option)
    element_input.click()

    # Chon option
    #Lay ra danh sach options
    xpath_options = '//input[@id="formBSX"]/div[2]/div[2]/select/option'
    option_elements = driver.find_elements(By.XPATH, xpath_options)
    for i_element in option_elements:
        str_option = str(i_element.text)
        if str_option == 'Xe máy':
            i_element.click()
            break

def xu_ly_captcha(driver):
    """Xử lý captchaimage"""
    # su dung thu vien pyteseract de trich xuat hinh anh sang text 
    # 1. save the image sang hinh anh
    element = driver.find.element(By.ID, '')
    element.screenshot('captcha.png')
    # 2. su dung thu vien de trich xuat sang text
    # 3. Tuong tac voi the input captcha: Nhap captcha
    # 4. submit tra cuu

def kiem_tra_ket_qua(driver):
    """Kiem tra ket qua captcha"""
    # 1. Trich xuat ket qua

    # 2. In ra loi phat nguoi hoac khong co loi

def main():
    """Handel tra cuu phat nguoi"""
    driver = open_chorme()
    
    xu_ly_bien_kiem_soat(driver)

    xu_ly_loai_phuong_tien(driver)

    xu_ly_captcha(driver)

    kiem_tra_ket_qua(driver)