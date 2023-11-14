## 本文件用于制作各种数据集和相关辅助文件
###  [generatebackground](generatebackground)
    用与制作在图像分类任务中，无缺陷的这一类图片
    过程：
    1.人工标记无缺陷区域
    2.通过脚本将无缺陷区域裁成想要的大小
### [tools](tools)
    通用的工具
    [visualizeXml.py](tools%2FvisualizeXml.py) xml标签可视化
    [deleteEmptyXml.py](tools%2FdeleteEmptyXml.py) 删除没有标记的xml文件
### [object2class](object2class)
    用分类的方法完成目标检测任务，该文件夹根据xml文件和图像，制作图像分类数据集
    [ob2cl.py](object2class%2Fob2cl.py) 依据窗口与缺陷位置的交并比关系，制作背景与缺陷的分类数据集
### [sepdata](sepdata)
    用于分割数据集
    [directSepImg.py](sepdata%2FdirectSepImg.py) 按照比例随机分配训练集和验证集，注意：只对图片进行分配
    [sepbyxml.py](sepdata%2Fsepbyxml.py) 以xml标记文件为参照，按照比例随机分配训练集和验证集
### [makeclsdata](makeclsdata)
    用于制作分类数据集
    [convertClsFile2ClsTxt.py](makeclsdata%2FconvertClsFile2ClsTxt.py) 问价夹格式转化txt标记格式，注意标签要0开始标号
    [makeclsbycopycls.py](makeclsdata%2Fmakeclsbycopycls.py) 需求场景：需要数据增强等操作后的数据集与原数集对比实验；
    通过读取原数据集的文件名称构建增强数据集
    