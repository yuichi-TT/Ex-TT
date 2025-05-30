# 5. Viết hàm kiểm tra xem trong chuỗi có ký tự số hay không. Nếu có, tách các số đó ra thành một mảng riêng.
def extract_numbers(text):
    # Kiểm tra xem có ký tự số hay không
    has_digit = any(char.isdigit() for char in text)
    
    if not has_digit:
        return "Chuỗi không chứa ký tự số."
    
    # Tách các số thành mảng
    numbers = [char for char in text if char.isdigit()]
    
    return numbers

# Test chương trình
text = input("Nhập chuỗi: ")
result = extract_numbers(text)
print("Kết quả:", result)