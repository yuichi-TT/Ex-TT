import pandas as pd
import numpy as np

print("=== BÀI TẬP PYTHON PANDAS 1 ===")
print("Bài 1: Tạo và thao tác với DataFrame\n")

# Tạo DataFrame với thông tin 10 sinh viên
data_dict = {
    'Name': ['Nguyễn Văn An', 'Trần Thị Bình', 'Lê Văn Cường', 'Phạm Thị Dung', 
             'Hoàng Văn Em', 'Vũ Thị Phương', 'Đỗ Văn Giang', 'Bùi Thị Hoa',
             'Ngô Văn Inh', 'Lý Thị Kim'],
    'Age': [20, 19, 21, 20, 22, 19, 20, 21, 19, 20],
    'Gender': ['Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ'],
    'Score': [8.5, 6.2, 4.8, 7.3, 9.1, 5.5, 3.2, 8.8, 6.7, 7.9]
}

df_students = pd.DataFrame(data_dict)

print("1. HIỂN THỊ DỮ LIỆU:")
print("=" * 50)

# a) Hiển thị toàn bộ dữ liệu của bảng
print("a) Toàn bộ dữ liệu của bảng:")
print(df_students)
print()

# b) 3 dòng đầu tiên
print("b) 3 dòng đầu tiên:")
print(df_students.head(3))
print()

# c) Theo index=2 và cột Name
print("c) Theo index=2 và cột Name:")
try:
    print(df_students.loc[2, 'Name'])
except KeyError as e:
    print(f"Lỗi: {e}")
print()

# d) Theo index=10 và cột Age (sẽ có lỗi vì chỉ có index 0-9)
print("d) Theo index=10 và cột Age:")
try:
    print(df_students.loc[10, 'Age'])
except KeyError as e:
    print(f"Lỗi: Index 10 không tồn tại (chỉ có index từ 0-9)")
print()

# e) Các cột Name và Score
print("e) Các cột Name và Score:")
print(df_students[['Name', 'Score']])
print()

print("2. THÊM CỘT PASS:")
print("=" * 50)

# Thêm cột Pass với điều kiện Score >= 5
df_students['Pass'] = df_students['Score'] >= 5

print("DataFrame sau khi thêm cột Pass:")
print(df_students)
print()

print("3. SẮP XẾP THEO ĐIỂM:")
print("=" * 50)

# Sắp xếp theo Score giảm dần
df_sorted = df_students.sort_values('Score', ascending=False)

print("Danh sách sinh viên sắp xếp theo điểm Score giảm dần:")
print(df_sorted)
print()

print("4. THỐNG KÊ THÊM:")
print("=" * 50)

# Một số thống kê bổ sung
print(f"Số sinh viên đậu (Pass = True): {df_students['Pass'].sum()}")
print(f"Số sinh viên rớt (Pass = False): {(~df_students['Pass']).sum()}")
print(f"Điểm trung bình: {df_students['Score'].mean():.2f}")
print(f"Điểm cao nhất: {df_students['Score'].max()}")
print(f"Điểm thấp nhất: {df_students['Score'].min()}")

print("\nSinh viên có điểm cao nhất:")
top_student = df_students[df_students['Score'] == df_students['Score'].max()]
print(top_student[['Name', 'Score']])

print("\nSinh viên có điểm thấp nhất:")
lowest_student = df_students[df_students['Score'] == df_students['Score'].min()]
print(lowest_student[['Name', 'Score']])
