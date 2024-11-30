import pickle
import os
import numpy as np

# Đường dẫn đến file .pkl
file_path = "embeddings/6745ac062b7a4e0415cbaec5_lequoctrieu618@gmail.com.pkl"  # Thay "path/to/your/file.pkl" bằng đường dẫn thực tế

with open(file_path, 'rb') as f:
    data = pickle.load(f)

# Kiểm tra kích thước của từng vector
if isinstance(data, list) and all(isinstance(vec, list) for vec in data):
    print(f"Number of vectors: {len(data)}")
    print(f"Dimension of vectors: {len(data[0])}")
else:
    print("Dữ liệu không hợp lệ hoặc không phải danh sách các vector.")

# Chuyển sang numpy array để kiểm tra thêm
data_np = np.array(data)

# Hiển thị thống kê cơ bản
print("Statistics:")
print(f"Min value: {np.min(data_np)}")
print(f"Max value: {np.max(data_np)}")
print(f"Mean value: {np.mean(data_np)}")
print(f"Standard deviation: {np.std(data_np)}")

# Kiểm tra chiều của tất cả vector
consistent_dimensions = all(len(vec) == len(data[0]) for vec in data)
if consistent_dimensions:
    print("Tất cả vector có cùng kích thước.")
else:
    print("Vector không đồng nhất về kích thước.")