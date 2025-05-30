# 8. Viết chương trình đổi chữ xen kẽ: một chữ hoa và một chữ thường.
#  Ví dụ: nhập "ABCDEfgh" → xuất: "AbCdEfGh"
def alternate_case(text):
    # Chuyển chuỗi thành danh sách các ký tự
    result = []
    
    # Duyệt qua từng ký tự và chỉ số
    for i, char in enumerate(text):
        if i % 2 == 0:  # Vị trí chẵn: chữ hoa
            result.append(char.upper())
        else:  # Vị trí lẻ: chữ thường
            result.append(char.lower())
    
    # Nối các ký tự lại thành chuỗi
    return "".join(result)

# Test chương trình
text = input("Nhập chuỗi: ")
print("Kết quả:", alternate_case(text))