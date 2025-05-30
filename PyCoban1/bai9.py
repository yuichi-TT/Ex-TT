# 9. Viết chương trình nhập vào một chuỗi ký tự, kiểm tra xem chuỗi đó có đối xứng không.
#  Chuỗi đối xứng là chuỗi mà khi viết ngược lại vẫn giống như ban đầu.
def is_palindrome(text):
    # Chuyển chuỗi thành chữ thường và loại bỏ khoảng trắng, dấu câu
    cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
    
    # So sánh chuỗi với chuỗi đảo ngược
    return cleaned_text == cleaned_text[::-1]

# Test chương trình
text = input("Nhập chuỗi: ")
if is_palindrome(text):
    print("Chuỗi là chuỗi đối xứng.")
else:
    print("Chuỗi không phải là chuỗi đối xứng.")