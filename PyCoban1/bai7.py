# 7. Viết chương trình chuyển ký tự đầu tiên của mỗi từ trong chuỗi thành chữ in hoa.
def capitalize_words(text):
    # Tách chuỗi thành danh sách các từ
    words = text.split()
    
    # Chuyển ký tự đầu của mỗi từ thành chữ in hoa
    capitalized_words = [word.capitalize() for word in words]
    
    # Nối các từ lại thành chuỗi
    return " ".join(capitalized_words)

# Test chương trình
text = input("Nhập chuỗi: ")
print("Kết quả:", capitalize_words(text))