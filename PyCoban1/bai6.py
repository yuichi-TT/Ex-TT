# 6. Viết hàm cắt chuỗi họ tên thành chuỗi họ lót và chuỗi tên.
def split_name(full_name):
    # Loại bỏ khoảng trắng thừa và tách chuỗi thành danh sách các từ
    words = full_name.strip().split()
    
    # Nếu chuỗi rỗng hoặc không đủ từ
    if not words:
        return "Chuỗi rỗng.", ""
    if len(words) == 1:
        return "", words[0]
    
    # Lấy họ lót (tất cả trừ từ cuối) và tên (từ cuối)
    ho_lot = " ".join(words[:-1])
    ten = words[-1]
    
    return ho_lot, ten

# Test chương trình
full_name = input("Nhập họ tên: ")
ho_lot, ten = split_name(full_name)
print(f"Họ lót: {ho_lot}")
print(f"Tên: {ten}")