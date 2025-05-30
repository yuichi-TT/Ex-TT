# 2. Viết chương trình đảo ngược thứ tự các từ có trong chuỗi.
#  Ví dụ: nhập "lap trinh bang ngon ngu python" → xuất: "python ngu ngon bang trinh lap"
def reverse_words(text):
    # Tách chuỗi thành danh sách các từ
    words = text.split()
    
    # Đảo ngược danh sách các từ
    words.reverse()
    
    # Nối các từ lại thành chuỗi
    return " ".join(words)

# Test chương trình
text = input("Nhập chuỗi: ")
print("Kết quả:", reverse_words(text))