# 10. Viết chương trình nhập vào một số có 3 chữ số, xuất ra dòng chữ mô tả giá trị con số đó.
#  Ví dụ: nhập 123 → xuất: "một trăm hai mươi ba"
def number_to_text(number):
    # Từ điển ánh xạ số sang chữ
    ones = ["", "một", "hai", "ba", "tư", "năm", "sáu", "bảy", "tám", "chín"]
    tens = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", 
            "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
    
    # Kiểm tra số có 3 chữ số hay không
    if not (100 <= number <= 999):
        return "Vui lòng nhập số có 3 chữ số."
    
    # Tách số thành hàng trăm, chục, đơn vị
    hundreds = number // 100
    tens_digit = (number % 100) // 10
    ones_digit = number % 10
    
    # Xây dựng chuỗi mô tả
    result = ones[hundreds] + " trăm"
    
    # Xử lý hàng chục và đơn vị
    if tens_digit == 0:
        if ones_digit != 0:
            result += " lẻ " + ones[ones_digit]
    else:
        result += " " + tens[tens_digit]
        if ones_digit != 0:
            # Xử lý trường hợp "mốt" và "lăm"
            if ones_digit == 1:
                result += " mốt"
            elif ones_digit == 5:
                result += " lăm"
            else:
                result += " " + ones[ones_digit]
    
    return result.strip()