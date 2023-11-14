import numpy as np
import cv2  # 如果使用OpenCV

# from PIL import Image  # 如果使用PIL

# 从.npyz文件中加载数据
data = np.load('samples_640x64x64x3.npz')

# 循环遍历图像数据并将其还原为图像
for i, image_data in enumerate(data.files):
    image_array = data[image_data]
    for j,img in enumerate(image_array):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换颜色通道（BGR到RGB）
        cv2.imwrite(f'output\image_{j}.png', image)  # 保存为图像文件

    # 如果使用PIL，将NumPy数组转换为图像并保存
    # image = Image.fromarray(image_array)
    # image.save(f'image_{i}.png')
