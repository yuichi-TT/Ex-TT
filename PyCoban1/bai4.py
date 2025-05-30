# 4. Viết chương trình nhập một chuỗi bất kỳ, liệt kê số lần xuất hiện của mỗi ký tự.
def count_characters(text):
    # Tạo từ điển để đếm số lần xuất hiện của mỗi ký tự
    char_count = {}
    
    # Đếm số lần xuất hiện của mỗi ký tự
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1
    
    # In kết quả
    if not char_count:
        return "Chuỗi rỗng."
    
    print("Số lần xuất hiện của mỗi ký tự:")
    for char, count in char_count.items():
        print(f"Ký tự '{char}': {count} lần")

# Test chương trình
text = input("Nhập chuỗi: ")
count_characters(text)