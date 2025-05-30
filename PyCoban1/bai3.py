# 3. Viết chương trình tìm kiếm ký tự xuất hiện nhiều nhất trong chuỗi.
def most_frequent_char(text):
    # Tạo từ điển để đếm số lần xuất hiện của mỗi ký tự
    char_count = {}
    
    # Đếm số lần xuất hiện của mỗi ký tự
    for char in text:
        if char != ' ':  # Bỏ qua dấu cách (tùy chọn)
            char_count[char] = char_count.get(char, 0) + 1
    
    # Nếu chuỗi rỗng hoặc chỉ có dấu cách
    if not char_count:
        return "Không có ký tự nào trong chuỗi."
    
    # Tìm ký tự có số lần xuất hiện lớn nhất
    max_char = max(char_count, key=char_count.get)
    max_count = char_count[max_char]
    
    return f"Ký tự xuất hiện nhiều nhất là '{max_char}' với {max_count} lần."

# Test chương trình
text = input("Nhập chuỗi: ")
print(most_frequent_char(text))