import pandas as pd
import numpy as np

# Tạo bảng Nhân viên
data_nhanvien = {
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
}
df_nhanvien = pd.DataFrame(data_nhanvien)

# Tạo bảng Phòng ban
data_phongban = {
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
}
df_phongban = pd.DataFrame(data_phongban)

print("Bảng Nhân viên ban đầu:")
print(df_nhanvien)
print("\nBảng Phòng ban ban đầu:")
print(df_phongban)
print("-" * 30)

# 1. Kiểm tra các ô dữ liệu bị thiếu trong bảng Nhân viên
print("\n1. Kiểm tra dữ liệu bị thiếu trong bảng Nhân viên:")
print(df_nhanvien.isnull().sum())
print("-" * 30)

# 2. Xoá các dòng trong bảng Nhân viên nếu dòng đó có hơn 2 giá trị bị thiếu
# (Một dòng có tối đa 5 cột, nếu hơn 2 giá trị thiếu nghĩa là còn lại ít hơn 5-2 = 3 giá trị không thiếu)
# thresh = số lượng giá trị không thiếu tối thiểu để giữ lại dòng đó.
# Ở đây, cột ID không bao giờ thiếu. Các cột còn lại là Name, Age, Department, Salary (4 cột).
# Nếu một dòng có hơn 2 giá trị bị thiếu trong 4 cột này, thì nó có 3 hoặc 4 giá trị thiếu.
# Hoặc hiểu là, giữ lại dòng nếu nó có ít nhất (số cột - 2) giá trị không thiếu.
# Trong trường hợp này, tổng số cột là 5. Giữ lại nếu có ít nhất 5-2 = 3 giá trị không thiếu.
df_nhanvien_cleaned = df_nhanvien.dropna(thresh=len(df_nhanvien.columns) - 2)
print("\n2. Bảng Nhân viên sau khi xóa dòng có hơn 2 giá trị thiếu:")
print(df_nhanvien_cleaned)
print("-" * 30)

# Cập nhật df_nhanvien để các bước sau sử dụng bảng đã được làm sạch
df_nhanvien = df_nhanvien_cleaned.copy() # Sử dụng copy để tránh SettingWithCopyWarning

# 3. Điền giá trị cho các ô bị thiếu
# Name: thay bằng "Chưa rõ"
df_nhanvien['Name'].fillna("Chưa rõ", inplace=True)

# Age: thay bằng giá trị trung bình của cột Age
mean_age = df_nhanvien['Age'].mean()
df_nhanvien['Age'].fillna(mean_age, inplace=True)

# Salary: thay bằng giá trị nằm trước đó của ô bị thiếu của cột Salary
df_nhanvien['Salary'].fillna(method='ffill', inplace=True) # ffill: forward fill

# Department: thay bằng "Unknown"
df_nhanvien['Department'].fillna("Unknown", inplace=True)

print("\n3. Bảng Nhân viên sau khi điền giá trị thiếu:")
print(df_nhanvien)
print("-" * 30)

# 4. Chuyển kiểu dữ liệu của Age và Salary sang int
# Đảm bảo rằng không còn NaN trong Age và Salary trước khi chuyển đổi
# Age có thể là float sau khi tính mean, cần làm tròn trước khi chuyển sang int nếu muốn
df_nhanvien['Age'] = df_nhanvien['Age'].round().astype(int)
df_nhanvien['Salary'] = df_nhanvien['Salary'].astype(int)

print("\n4. Bảng Nhân viên sau khi chuyển kiểu dữ liệu Age và Salary sang int:")
print(df_nhanvien.info())
print(df_nhanvien)
print("-" * 30)

# 5. Tạo cột mới Salary_after_tax: giá trị sẽ là cột Salary - 10% thuế
df_nhanvien['Salary_after_tax'] = df_nhanvien['Salary'] - (df_nhanvien['Salary'] * 0.10)
print("\n5. Bảng Nhân viên với cột Salary_after_tax:")
print(df_nhanvien)
print("-" * 30)

# 6. Lọc ra các nhân viên thuộc phòng IT và có tuổi lớn hơn 25
it_employees_over_25 = df_nhanvien[(df_nhanvien['Department'] == 'IT') & (df_nhanvien['Age'] > 25)]
print("\n6. Nhân viên thuộc phòng IT và có tuổi lớn hơn 25:")
print(it_employees_over_25)
print("-" * 30)

# 7. Sắp xếp bảng nhân viên theo Salary_after_tax giảm dần
df_nhanvien_sorted = df_nhanvien.sort_values(by='Salary_after_tax', ascending=False)
print("\n7. Bảng Nhân viên sắp xếp theo Salary_after_tax giảm dần:")
print(df_nhanvien_sorted)
print("-" * 30)

# 8. Nhóm nhân viên theo Department và tính mức lương trung bình cho từng phòng ban
average_salary_by_department = df_nhanvien.groupby('Department')['Salary'].mean().reset_index()
print("\n8. Mức lương trung bình theo từng phòng ban:")
print(average_salary_by_department)
print("-" * 30)

# 9. Dùng merge() để nối bảng nhân viên với bảng quản lý phòng ban
df_merged = pd.merge(df_nhanvien, df_phongban, on='Department', how='left')
print("\n9. Bảng Nhân viên sau khi merge với bảng Phòng ban:")
print(df_merged)
print("-" * 30)

# 10. Tạo bảng Nhân viên Mới gồm 2 nhân viên mới và dùng concat() để thêm họ vào bảng Nhân viên
new_employees_data = {
    'ID': [107, 108],
    'Name': ['Giang', 'Hoàng'],
    'Age': [29, 31],
    'Department': ['Marketing', 'IT'],
    'Salary': [900, 950]
    # Salary_after_tax sẽ được tính sau khi concat hoặc điền NaN rồi tính lại
}
df_new_employees = pd.DataFrame(new_employees_data)

# Để concat, các cột nên giống nhau. Tính Salary_after_tax cho nhân viên mới
df_new_employees['Salary_after_tax'] = df_new_employees['Salary'] - (df_new_employees['Salary'] * 0.10)


df_nhanvien_final = pd.concat([df_merged, df_new_employees], ignore_index=True)

# Nếu muốn tính lại Salary_after_tax cho toàn bộ bảng sau khi concat nếu có NaN từ merge
# (ví dụ: nếu nhân viên mới có Department không có trong df_phongban, Manager sẽ là NaN)
# df_nhanvien_final['Salary_after_tax'] = df_nhanvien_final['Salary'] - (df_nhanvien_final['Salary'] * 0.10)
# Và điền NaN cho cột Manager nếu cần, ví dụ:
df_nhanvien_final['Manager'].fillna('Chưa có', inplace=True)


print("\n10. Bảng Nhân viên sau khi thêm 2 nhân viên mới:")
print(df_nhanvien_final)
print("-" * 30)