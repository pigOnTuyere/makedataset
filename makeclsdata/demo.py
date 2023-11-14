import os

def get_all_folders(directory):
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return folders

# 指定目录路径
directory_path = "D:\code\Makedataset\data"

# 获取目录下所有文件夹名
folders = get_all_folders(directory_path)

# 打印结果
print("All folders in the directory:")
for folder in folders:
    print(folder)
