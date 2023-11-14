import xml.dom.minidom
import cv2
import os
import xml.etree.ElementTree as ET
import numpy as np

"""
该脚本用制作分类数据集
imgPath：输入图片路径
imgAnn：输入标记框路径
resultPath：生成可视化图片路径
"""

# 样本图片路径
imgPath = 'C:\\Users\jack\Desktop\defect\gangb_2\data\images'
# 样本图片标签
imgAnn = 'C:\\Users\jack\Desktop\defect\gangb_2\data\\ann'


bgpath = "makdata"
defectPath = 'makdata'

# 检查路径是否存在
if not os.path.exists(bgpath):
    # 如果路径不存在，创建它
    os.makedirs(bgpath)
    print(f"路径 {bgpath} 不存在，已成功创建。")
else:
    print(f"路径 {bgpath} 已经存在。")

if not os.path.exists(defectPath):
    # 如果路径不存在，创建它
    os.makedirs(defectPath)
    print(f"路径 {defectPath} 不存在，已成功创建。")
else:
    print(f"路径 {defectPath} 已经存在。")

# keymaps ={'beijing':0,'cr':1,'4_shuiban':2,'6_siban':3,'7_yiwu':4,'8_yahen':5,'9_zhehen':6,'3_yueyawan':7}
# keymaps_2 = {0:'beijing',1:'cr',2:'4_shuiban',3:'6_siban',4:'7_yiwu',5:'8_yahen',6:'9_zhehen',7:'3_yueyawan'}

keymaps = {'bg':0,'defect':1}
keymaps_2 = {0:'bg',1:'defect'}

imglist = os.listdir(imgPath)
xmllist = os.listdir(imgAnn)


def cal_intersection(box1, box2):
    """
    :param box1: = [xmin1, xmax1, ymin1, ymax1]
    :param box2: = [xmin2, xmax2, ymin2, ymax2]
    :return:
    """
    xmin1, xmax1, ymin1, ymax1 = box1
    xmin2, xmax2, ymin2, ymax2 = box2

    # 计算每个矩形的面积
    s1 = (xmax1 - xmin1) * (ymax1 - ymin1)  # b1的面积
    s2 = (xmax2 - xmin2) * (ymax2 - ymin2)  # b2的面积

    # 计算相交矩形
    xmin = max(xmin1, xmin2)
    ymin = max(ymin1, ymin2)
    xmax = min(xmax1, xmax2)
    ymax = min(ymax1, ymax2)

    w = max(0, xmax - xmin)
    h = max(0, ymax - ymin)
    intersection = w * h  # C∩G的面积

    return intersection

class obejct2cls(object):
    def __init__(self,imgPath,xmlPath):
        '''

        :param imgPath:
        :param xmlPath:
        :param outpath:
        '''

        self.rh = 1200                      # 定义缩放后的图像的高
        self.rw = 1600                      # 定义缩放后的图像的宽
        self.imgpath = imgPath              # 图像的输入文件夹
        self.xmlpath = xmlPath              # xml标签文件所在文件夹
        self.ch = 200                       # 裁剪后的图像的高
        self.cw = 200                       # 裁剪后的图像的宽
        self.img = cv2.imread(self.imgpath)
        self.resizeImg = cv2.resize(self.img, (self.rw, self.rh))

    def generate_class_data(self):
        resizeImg = self.resizeImg
        bboxs = []
        cls   = []
        # 检查是否存在对应的标签文集
        if os.path.exists(self.xmlpath):
            tree = ET.parse(self.xmlpath)
            root = tree.getroot()
            # 获取bbox的坐标
            for object in root.findall('object'):
                object_name = object.find('name').text
                Xmin = int(object.find('bndbox').find('xmin').text)
                Ymin = int(object.find('bndbox').find('ymin').text)
                Xmax = int(object.find('bndbox').find('xmax').text)
                Ymax = int(object.find('bndbox').find('ymax').text)

                # 坐标变换
                Xmin, Xmax, Ymin, Ymax = self.sale_point((Xmin, Xmax, Ymin, Ymax))
                bboxs.append([Xmin, Xmax, Ymin, Ymax])
                cls.append(keymaps[object_name])

                # 以下代码用于调试
                #color = (4, 250, 7)
                #cv2.rectangle(resizeImg, (Xmin, Ymin), (Xmax, Ymax), color, 2)
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(resizeImg, object_name, (Xmin, Ymin - 7), font, 0.5, (6, 230, 230), 2)
            # 裁剪图像，并为图像制作标签和裁剪
            self.generate_label(bboxs,cls)
            #
        else:  # 不存在标签文件时，直接对图像进行裁剪
            self.bg_crop()
            print(f"文件 '{self.xmlpath}' 不存在.")

    def sale_point(self,point):

        img = self.img
        h,w,_ =img.shape

        Xmin, Xmax, Ymin, Ymax = point
        Xmin = Xmin * self.rw/w
        Xmax = Xmax * self.rw/w
        Ymin = Ymin * self.rh/h
        Ymax = Ymax * self.rh/h
        # return Xmin, Xmax, Ymin, Ymax
        return int(Xmin), int(Xmax), int(Ymin), int(Ymax)

    def generate_label(self,bboxs,cls):
        rw = self.rw
        cw = self.cw
        rh = self.rh
        ch = self.ch
        img = self.resizeImg

        # 获取图像前缀名
        filename =os.path.basename(self.imgpath)
        basename =os.path.splitext(filename)[0]
        cropimg_num = 1

        if rw % cw == 0 and rh % ch == 0:
            for y in range(0, rh, ch):
                for x in range(0, rw, cw):
                    # 计算窗口的坐标
                    w_xmin, w_ymin = x, y
                    w_xmax, w_ymax = x + cw, y + ch
                    intersections = []
                    # 计算窗口与所有box的交集面积
                    for i, bbox in enumerate(bboxs):
                        intersection = cal_intersection(bbox, [w_xmin, w_xmax, w_ymin, w_ymax])
                        intersections.append(intersection)
                    # 若缺陷面积大于25^2,将会被裁剪为缺陷
                    maxArea = max(intersections)
                    # 下面的方法，max_index只会获去一个值
                    max_index = intersections.index(maxArea)
                    if maxArea > 25 ** 2:
                        # 获取缺陷的类型
                        cl = cls[max_index]
                    else:
                        cl = 0
                    # 提取窗口图像
                    window = img[w_ymin:w_ymax, w_xmin:w_xmax]
                    # 写入图像，根据是否是缺陷和背景写入不同的文件夹
                    if cl==0:
                        file_path = bgpath + '/' + keymaps_2[cl] + '_{}_'.format(cropimg_num) + filename
                    else:
                        file_path = defectPath + '/' + keymaps_2[cl] + '_{}_'.format(cropimg_num) + filename

                    cropimg_num += 1
                    cv2.imwrite(file_path, window)
        else:
            print('参数输入错误，无法恰好裁剪')

    def bg_crop(self):
        rw = self.rw
        cw = self.cw
        rh = self.rh
        ch = self.ch
        img = self.resizeImg

        # 获取图像前缀名
        filename = os.path.basename(self.imgpath)
        basename = os.path.splitext(filename)[0]
        cropimg_num = 1

        if rw % cw == 0 and rh % ch == 0:
            for y in range(0, rh, ch):
                for x in range(0, rw, cw):
                    # 计算窗口的坐标
                    w_xmin, w_ymin = x, y
                    w_xmax, w_ymax = x + cw, y + ch
                    window = img[w_ymin:w_ymax, w_xmin:w_xmax]
                    # 写入图像
                    file_path = bgpath + '/' + keymaps_2[0] + '_{}_'.format(cropimg_num) + filename
                    cropimg_num += 1
                    cv2.imwrite(file_path, window)
        else:
            print('参数输入错误，无法恰好裁剪')



if __name__ == "__main__":

    for i in range(len(imglist)):
        # 每个图像全路径
        image_input_fullname = imgPath + '/' + imglist[i]
        # 使用os.path.splitext来分割文件名和扩展名，并提取基本文件名
        basename = os.path.splitext(imglist[i])[0]
        xml_input_fullname = imgAnn + '/' + basename + '.xml'
        ob2cls = obejct2cls(image_input_fullname,xml_input_fullname)
        ob2cls.generate_class_data()


