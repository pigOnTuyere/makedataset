import xml.dom.minidom
import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np

"""
该脚本用于目标框可视化
imgPath：输入图片路径
imgAnn：输入标记框路径
resultPath：生成可视化图片路径
"""

# 样本图片路径
imgPath = 'GC10_DET/images/images/crease'
# 样本图片标签
imgAnn = 'GC10_DET/label/label'
# 输出结果保存路径
resultPath = 'output'
os.mkdir(resultPath)


imglist = os.listdir(imgPath)
xmllist = os.listdir(imgAnn)






if __name__ == "__main__":

    for i in range(len(imglist)):
        # 每个图像全路径
        image_input_fullname = imgPath + '/' + imglist[i]
        # 使用os.path.splitext来分割文件名和扩展名，并提取基本文件名
        basename = os.path.splitext(imglist[i])[0]
        xml_input_fullname = imgAnn + '/' + basename + '.xml'
        image_output_fullname = resultPath + '/' + imglist[i]

        img = cv2.imread(image_input_fullname)

        # 判断是否存在对应标签
        if os.path.exists(xml_input_fullname):

            dom = xml.dom.minidom.parse(xml_input_fullname)
            tree = ET.parse(xml_input_fullname)
            root = tree.getroot()

            for object in root.findall('object'):
                object_name = object.find('name').text
                Xmin = int(object.find('bndbox').find('xmin').text)
                Ymin = int(object.find('bndbox').find('ymin').text)
                Xmax = int(object.find('bndbox').find('xmax').text)
                Ymax = int(object.find('bndbox').find('ymax').text)
                color = (4, 250, 7)
                cv2.rectangle(img, (Xmin, Ymin), (Xmax, Ymax), color, 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, object_name, (Xmin, Ymin - 7), font, 0.5, (6, 230, 230), 2)



            # 获取图像
            cv2.imwrite(image_output_fullname, img)
        else: # 不存在标签文件时，直接保存图像
            cv2.imwrite(image_output_fullname, img)
            print(f"文件 '{xml_input_fullname}' 不存在.")
