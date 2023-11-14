import os

def read_images_with_labels(folder_path,an_path):
    '''

    :param folder_path:
    :param an_path:
    :return: 标签（list）

    '''
    images = []
    labels = []
    file_names = []
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        # 检查是否为图片文件（可根据需要调整）
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # 从文件名中提取分类标签，这里假设文件名和标签之间用下划线分隔
            file_names.append(file_name)
            typeName = file_name[:file_name.rindex('_')]
            for idex, lb in enumerate(classes):
                if typeName == lb:
                    labels.append(idex)
                    break
                if typeName != lb and idex == 5:
                    print('error')
    # 使用"with open"语句打开文件，并以写入模式('w')写入数据
    with open(an_path, 'w') as file:
        # 使用循环遍历列表中的数据，并将每个数据写入一行
        for file_name, lb in zip(file_names, labels):
            file.write(str(file_name) + ' '+str(lb)+'\n')
    return  labels

if __name__ == '__main__':
    # 定义你自己的类别
    classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
    folder_path = 'NEU_CLS/images/val2017'  # 替换为实际的文件夹路径
    an_path = 'val2017.txt'
    labels = read_images_with_labels(folder_path, an_path)

