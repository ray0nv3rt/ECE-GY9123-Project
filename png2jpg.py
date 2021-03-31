import os
import sys
import os.path as osp
import shutil
from PIL import Image
import os.path as osp

def mkdirs(d):
    # if not osp.exists(d):
    if not osp.isdir(d):
        os.makedirs(d)
# input_folder = "/home/ckq/Desktop/MOT/images/train/0000/img"  # 源文件夹，包含.png格式图片
# output_folder = "/home/ckq/Desktop/MOT/images/train/0000/jpg"  # 输出文件夹
src_folder = "/media/ckq/data/kitti/MOT/images/train"  # 源文件夹，包含.png格式图片
dist_folder = "/media/ckq/data/kitti/MOT_new/images/train"  # 输出文件夹

src_folder_names=os.listdir(src_folder)
print(src_folder_names)
for src_folder_name in src_folder_names:
    input_folder = osp.join(src_folder,src_folder_name,'img1')
    #print(input_folder)
    output_folder = osp.join(dist_folder,src_folder_name,'img1')  # 输出文件夹
    if not os.path.isdir(output_folder):
        mkdirs(output_folder)
    else:  # 如果之前已经生成过: 递归删除目录和文件, 重新生成目录
        shutil.rmtree(output_folder)
        os.makedirs(output_folder)
    print(output_folder)
    a = []
    for root, dirs, files in os.walk(input_folder):
        for filename in (x for x in files if x.endswith('.png')):
            filepath = os.path.join(root, filename)

            object_class = filename.split('.')[0]
            a.append(object_class)
        print(a)

    for i in a:
        old_path = input_folder + "/" + str(i) + '.png'
        new_path = output_folder + "/" + str(i) + '.jpg'
        img = Image.open(old_path)
        img.save(new_path)
