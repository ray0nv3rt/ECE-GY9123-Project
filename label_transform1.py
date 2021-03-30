import os
import numpy as np
import pandas as pd
import os.path as osp


def replace(file, old_content, new_content):
    content = read_file(file)
    content = content.replace(old_content, new_content)
    rewrite_file(file, content)

# 读文件内容
def read_file(file):
    with open(file, encoding='UTF-8') as f:
        read_all = f.read()
        f.close()

    return read_all

# 写内容到文件
def rewrite_file(file, data):
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(data)
        f.close()

src_data='D:\\NYU\\git\\label_02'
seqs = [s for s in os.listdir(src_data)]
#print(seqs)
for seq in seqs:
    path=osp.join(src_data,seq)
    # seq_gt_path = osp.join(src_data, seq, 'gt/gt.txt')
    # print(seq_gt_path)
    # gt = np.loadtxt(seq_gt_path, dtype=np.str, delimiter=',')  # 加载成np格式
    # print(str(gt))
    replace(path, ' ', ',')
    replace(path, 'DontCare', '10')
    replace(path, 'Person', '1')
    replace(path, 'Pedestrian', '2')
    replace(path, 'Car', '3')
    replace(path, 'Person_sitting', '4')
    replace(path, 'Cyclist', '5')
    replace(path, 'Van', '6')
    replace(path, 'Truck', '7')
    replace(path, 'Tram', '8')
    replace(path, 'Misc', '9')
