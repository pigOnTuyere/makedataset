import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET

START_BOUNDING_BOX_ID = 1
save_path = "."


def get(root, name):
    return root.findall(name)


def get_and_check(root, name, length):
    vars = get(root, name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        # print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()

        filename = os.path.basename(xml_f)[:-4] + ".jpg"
        image_id = 20190000001 + index
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id': image_id}
        json_dict['images'].append(image)
        #  Currently we do not support segmentation
        segmented = get_and_check(root, 'segmented', 1).text
        assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in all_categories:
                all_categories[category] += 1
            else:
                all_categories[category] = 1
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print(
                    "[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(
                        category, pre_define_categories, new_id))
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
            assert (xmax > xmin), "xmax <= xmin, {}".format(line)
            assert (ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id':
                image_id, 'bbox': [xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'ball', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))
    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories),
                                                                                  all_categories.keys(),
                                                                                  len(pre_define_categories),
                                                                                  pre_define_categories.keys()))
    print("category: id --> {}".format(categories))
    print(categories.keys())
    print(categories.values())


if __name__ == '__main__':
    # 定义你自己的类别
    classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
    saved_coco_path = 'D:\code\MMLAB\\tools\\'
    img_path = 'D:\code\MMLAB\\tools\\NEU-DET_mod\IMAGES\\'
    # 初始文件所在的路径
    xml_dir = "D:\code\MMLAB\\tools\\NEU-DET_mod\\ANNOTATIONS\\"

    # 创建文件
    if not os.path.exists("%scoco/annotations/" % saved_coco_path):
        os.makedirs("%scoco/annotations/" % saved_coco_path)
    if not os.path.exists("%scoco/images/train2017/" % saved_coco_path):
        os.makedirs("%scoco/images/train2017" % saved_coco_path)
    if not os.path.exists("%scoco/images/val2017/" % saved_coco_path):
        os.makedirs("%scoco/images/val2017" % saved_coco_path)

    pre_define_categories = {}
    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i
    # 这里也可以自定义类别id，把上面的注释掉换成下面这行即可
    # pre_define_categories = {'a1': 1, 'a3': 2, 'a6': 3, 'a9': 4, "a10": 5}
    only_care_pre_define_categories = True  # or False

    # 保存的json文件
    save_json_train = '%scoco/annotations/instances_train2017.json' % saved_coco_path
    save_json_val = '%scoco/annotations/instances_val2017.json' % saved_coco_path
    #save_json_test = 'test_food.json'

    # 初始文件所在的路径
    xml_list = glob.glob(xml_dir + "/*.xml")
    xml_list = np.sort(xml_list)

    # 打乱数据集
    np.random.seed(100)
    np.random.shuffle(xml_list)

    ''''
    修改分配比例
    '''
    # 按比例划分打乱后的数据集
    train_ratio = 0.8
    val_ratio = 0.2
    train_num = int(len(xml_list) * train_ratio)
    val_num = int(len(xml_list) * val_ratio)
    xml_list_train = xml_list[:train_num]
    xml_list_val = xml_list[train_num: train_num + val_num]
    # xml_list_test = xml_list[train_num + val_num:]

    # 将xml文件转为coco文件，在指定目录下生成三个json文件（train/test/food）
    convert(xml_list_train, save_json_train)
    convert(xml_list_val, save_json_val)
    # convert(xml_list_test, save_json_test)

    # # 将图片按照划分后的结果进行存放
    # if os.path.exists(save_path + "/annotations"):
    #     shutil.rmtree(save_path + "/annotations")
    # os.makedirs(save_path + "/annotations")
    # if os.path.exists(save_path + "/images_divide/train"):
    #     shutil.rmtree(save_path + "/images_divide/train")
    # os.makedirs(save_path + "/images_divide/train")
    # if os.path.exists(save_path + "/images_divide/val"):
    #     shutil.rmtree(save_path + "/images_divide/val")
    # os.makedirs(save_path + "/images_divide/val")
    # if os.path.exists(save_path + "/images_divide/test"):
    #     shutil.rmtree(save_path + "/images_divide/test")
    # os.makedirs(save_path + "/images_divide/test")

    # # 按需执行，生成3个txt文件，存放相应的文件名称
    f1 = open( saved_coco_path+"train.txt", "w")
    for xml in xml_list_train:
        img = xml[:-4] + ".jpg"
        img = img_path + os.path.basename(img)
        f1.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, "%scoco/images/train2017" % saved_coco_path + '//' + os.path.basename(img))

    f2 = open( saved_coco_path+"val.txt", "w")
    for xml in xml_list_val:
        img = xml[:-4] + ".jpg"
        img = img_path + os.path.basename(img)
        f2.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, "%scoco/images/val2017/" % saved_coco_path + '//' + os.path.basename(img))

    # f3 = open("test.txt", "w")
    # for xml in xml_list_val:
    #     img = xml[:-4] + ".jpg"
    #     f2.write(os.path.basename(xml)[:-4] + "\n")
    #     shutil.copyfile(img, save_path + "/images_divide/test/" + os.path.basename(img))
    #
    # f1.close()
    # f2.close()
    # f3.close()

    print("-" * 50)
    print("train number:", len(xml_list_train))
    print("val number:", len(xml_list_val))
    # print("test number:", len(xml_list_val))
