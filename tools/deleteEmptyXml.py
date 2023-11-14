import os
import xml.etree.ElementTree as ET

xmlPath = "D:\code\Makedataset\imgseg\data_4\\ann"
xmllist = os.listdir(xmlPath )


def check_and_delete_xml(xml_file, object_name):
    count = 1
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # 在XML结构中查找包含 object_name 的元素
    for element in root.iter():
        if element.tag == object_name:
            # 如果找到了该对象，则不删除XML文件
            return
    # 如果没有找到对象，则删除XML文件
    os.remove(xml_file)
    return count


if __name__=="__main__":
    num = 0
    for i in range(len(xmllist)):
        xml_fullpath = xmlPath + '/' +xmllist[i]
        # 判断是否存在对应路径
        if os.path.exists(xml_fullpath):
            count = check_and_delete_xml(xml_fullpath,'object')
            if count!=None:
                num = count+num

    print('一共删除{}个xml文件'.format(num))


