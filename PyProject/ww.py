def main():
    # 1: Lay du lieu dau vao
    # - Doc file excel dau vao
    # - Lay ra ma so thue, ma tra cuu, URL

    # 2: Truy cap trang web tra cuu hoa don dien tu tuong ung voi URL
    # - Mo chrome voi thu muc tai file download
    # - Vao URL tuong ung

    # 3: Tra cuu hoa don dien tu
    # - Nhap ma so thue
    # - Nhap ma tra cuu
    # - Nhan nut tra cuu

    # 4: Kiem tra ket qua tra cuu
    # - Xuat hien man hinh tai hoa don
    # - Xuat hien man hinh thong bao loi

    # 5: Tai hoa don
    # - Neu tra cuu thanh cong, tai hoa don ve may
    # - Neu tra cuu khong thanh cong thi thong bao loi bang logging hoac print
    
    # 6: Doc file hoa don
    # Doc file bang duong dan: path file xml

    # 7: Trich xuat thong tin hoa don va luu thanh file excel output
    # Lay ra noi dung file xml
    # Trich xuat cac thong tin theo yeu cau mo ta ow file huong dan FPT
    print()

if __name__ == "__main__":
    main()

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# df = pd.read_excel("input.xlsx")
# dict_input = {
#     "Mã số thuế": ["0304244470", "0304244471", "0304308445",  "", "" ,"" , "" , "" ,""],
#   "Mã tra cứu": ["r08e17y79g", "r46jvxmvxg","rzmwy1yo4g","B1