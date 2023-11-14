import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np
'''
 脚本功能
    1.获取缺席数据集中的小目标
    2.将小目标与背景图片进行随机位置融合
'''

# 样本图片路径
imgPath = 'D:\code\makedata\makeyolodate\\NEU-DET-offical-xml\\NEU-DET\IMAGES'
# 样本图片标签
imgAnn = 'D:\code\makedata\makeyolodate\\NEU-DET-offical-xml\\NEU-DET\ANNOTATIONS'
# 融合背景图片路径
bgimgPath = "bg"
# 输出结果保存路径
resultPath = 'miximg'

os.mkdir(resultPath)
# os.mkdir('test')
imglist = os.listdir(imgPath)
xmllist = os.listdir(imgAnn)
bgimglist = os.listdir(bgimgPath)
# 打乱背景图像
np.random.seed(100)
np.random.shuffle(bgimglist)


num = 0


def mix_img(imgPath,object,size=200):
    '''
    :param imgPath: 图形路径
    :param object: 裁剪对象
    :param size: 分割大小
    :return: 无返回值
    '''

    global num
    img = cv2.imread(imgPath)

    # 获取bbox坐标
    object_name = object.find('name').text
    Xmin = int(object.find('bndbox').find('xmin').text)
    Ymin = int(object.find('bndbox').find('ymin').text)
    Xmax = int(object.find('bndbox').find('xmax').text)
    Ymax = int(object.find('bndbox').find('ymax').text)

     # 判断bbox是否满足面积要求（小目标要求）
    W = Xmax - Xmin
    H = Ymax - Ymin
    area = W*H
    if area < 50 ** 2 and area > 25 ** 2:
        # 满足小目标要求，截取目标，融合到背景图像当中
        region = img[Ymin:Ymax, Xmin:Xmax]
        # image_yuv = cv2.cvtColor( region, cv2.COLOR_BGR2YUV)
        # # 对Y通道进行自适应直方图均衡化
        # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(3, 3))
        # image_yuv[:, :, 0] = clahe.apply(image_yuv[:, :, 0])
        # # 将图像转换回BGR颜色空间
        # region = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        tarPath = bgimgPath + '/' + bgimglist[num]
        tarImg = cv2.imread(tarPath)
        # 随机区域融合
        height, width, _ = tarImg.shape
        x = np.random.randint(0, int(width-W))
        y = np.random.randint(0, int(height-H))
        # 随机区域融合图像
        # 创建渐变掩码
        gradient_mask = np.zeros((H, W), dtype=np.uint8)
        # 在掩码中创建水平渐变
        for i in range(W):
            gradient_mask[:, i] = int(255 * (i+1) / W)

        #tarImg[y:y+H, x:x+W] = region
        savePath = resultPath + '/' + 'bg_{}_{}.jpg'.format(object_name,num)

        # 两个图片合成
        #temp=tarImg[y:y + H, x:x + W]
        #tarImg[y:y+H, x:x+W]=cv2.addWeighted(tarImg[y:y+H, x:x+W], 0.6,region, 0.4, 0)
        mixImg = cv2.addWeighted(tarImg[y:y+H, x:x+W], 0.5,region, 0.5, 0)
        mixImg = cv2.bitwise_and(mixImg, mixImg, mask=gradient_mask)

        tarImg[y:y + H, x:x + W] = mixImg
        # 降低图像对比度
        #tarImg = cv2.convertScaleAbs(tarImg, alpha=0.5, beta=100)

        # # 减少融合度
        # # 将图像转换为YUV颜色空间
        image_yuv = cv2.cvtColor( tarImg, cv2.COLOR_BGR2YUV)
        # 对Y通道进行自适应直方图均衡化
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(5, 5))
        image_yuv[:, :, 0] = clahe.apply(image_yuv[:, :, 0])
        # 将图像转换回BGR颜色空间
        tarImg = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        num = num + 1
        # 保存合成后的图像
        cv2.imwrite(savePath,tarImg)
    else:
        return





if __name__ == "__main__":

    for i in range(len(imglist)):
        # 每个图像全路径
        image_input_fullname = imgPath + '/' + imglist[i]
        # 使用os.path.splitext来分割文件名和扩展名，并提取基本文件名
        basename = os.path.splitext(imglist[i])[0]
        xml_input_fullname = imgAnn + '/' + basename + '.xml'
        image_output_fullname = resultPath + '/' + imglist[i]

        img = cv2.imread(image_input_fullname)



        im = cv2.imread(image_input_fullname)

        # 判断是否存在无效标签文件
        if os.path.exists(xml_input_fullname):

            tree = ET.parse(xml_input_fullname)
            root = tree.getroot()
            objects = root.findall('object')

            for object in objects:
                mix_img(image_input_fullname,object)

