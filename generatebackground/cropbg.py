import xml.dom.minidom
import cv2
import os
import xml.etree.ElementTree as ET

'''
 脚本功能
    1.获取图形背景区域
    2.将背景区域拆分成指定大小
'''

# 样本图片路径
imgPath = 'GC10_DET/images/images/silk_spot'
# 样本图片标签
imgAnn = 'GC10_DET/label/label'
# 输出结果保存路径
resultPath = 'bg'

#os.mkdir(resultPath)
# os.mkdir('test')
imglist = os.listdir(imgPath)
xmllist = os.listdir(imgAnn)




cropimg_num = 0


def crop_img(imgPath,object,size=200):
    '''
    :param imgPath: 图形路径
    :param object: 裁剪对象
    :param size: 分割大小
    :return: 无返回值
    '''
    object_name = object.find('name').text
    Xmin = int(object.find('bndbox').find('xmin').text)
    Ymin = int(object.find('bndbox').find('ymin').text)
    Xmax = int(object.find('bndbox').find('xmax').text)
    Ymax = int(object.find('bndbox').find('ymax').text)

    global cropimg_num

    w = Xmax - Xmin
    H = Ymax - Ymin
    img = cv2.imread(imgPath)
    # 用于调试的代码
    #cv2.imwrite('test/test_{}.jpg'.format(cropimg_num), img[Ymin:Ymax, Xmin:Xmax])

    if w>size and H>size:
        w_num = int(w/size)
        H_num = int(H/size)
        for i in range(H_num):
            for j in range(w_num):
                cropped_region =  img[Ymin+i*size:Ymin+(i+1)*size, Xmin+j*size:Xmin+(j+1)*size]
                cropimg_num += 1
                file_path = resultPath + '/' + 'bg_silk_spot_{}.jpg'.format(cropimg_num)
                cv2.imwrite(file_path,cropped_region)

        #         # 用于测试
        #         color = (4, 250, 7)
        #         cv2.rectangle(img, (Xmin+j*size,Ymin+i*size), (Xmin+(j+1)*size, Ymin+(i+1)*size), color, 2)
        # cv2.imwrite('test/testline_{}.jpg'.format(cropimg_num), img)
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
                object_name = object.find('name').text
                if  object_name == 'cr':
                    crop_img(image_input_fullname,object)

