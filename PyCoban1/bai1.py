# 1. Viết chương trình đổi các từ ở đầu câu sang chữ hoa và những từ không phải đầu câu sang chữ thường.
#  Ví dụ: nGuYen vAN a → Nguyen Van A
def capitalize_sentence(text):
    # Tách câu thành các từ
    words = text.split()
    
    # Nếu không có từ, trả về chuỗi rỗng
    if not words:
        return ""
    
    # Xử lý từ đầu tiên: viết hoa chữ cái đầu
    result = [words[0].capitalize()]
    
    # Xử lý các từ còn lại: chuyển thành chữ thường
    for word in words[1:]:
        result.append(word.lower())
    
    # Nối các từ lại thành câu
    return " ".join(result)

# Test chương trình
text = input("Nhập câu: ")
print("Kết quả:", capitalize_sentence(text))