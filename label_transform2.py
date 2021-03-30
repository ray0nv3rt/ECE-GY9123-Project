import os.path as osp
import os
import shutil
import numpy as np


def mkdirs(d):
    # if not osp.exists(d):
    if not osp.isdir(d):
        os.makedirs(d)

data_root = '/media/ckq/data/kitti/'
seq_root = 'D:\\NYU\\git\\label_02'
label_root = 'D:\\NYU\\git\\label'

if not os.path.isdir(label_root):
    mkdirs(label_root)
else:  # 如果之前已经生成过: 递归删除目录和文件, 重新生成目录
    shutil.rmtree(label_root)
    os.makedirs(label_root)


cls_map = {
    'Person=1'
    'Pedestrian=2'
    'Car=3'
    'Person_sitting=4'
    'Cyclist=5'
    'Van=6'
    'Truck=7'
    'Tram=8'
    'Misc=9'
    'DontCare=10'
}

print("Dir %s made" % label_root)
seqs = [s for s in os.listdir(seq_root)]
#seqs=['0000.txt']

#打印序列
print(seqs)


tid_curr = 0
tid_last = -1
total_track_id_num = 0
for seq in seqs:  # 每段视频都对应一个gt.txt
    print("Process %s, " % seq, end='')

    # seq_info_path = osp.join(seq_root, seq, 'seqinfo.ini')   #提取每个数据的info信息 /media/ckq/data/kitti/MOT/images/train
    # #print(seq_info_path)
    # with open(seq_info_path) as seq_info_h:  # 读取 *.ini 文件
    #     seq_info = seq_info_h.read()
    #     seq_width = int(seq_info[seq_info.find('imWidth=') + 8:seq_info.find('\nimHeight')])  # 视频的宽
    #     seq_height = int(seq_info[seq_info.find('imHeight=') + 9:seq_info.find('\nimExt')])  # 视频的高
    #     #print('seq_width:',seq_width)
    #     #print('seq_height:', seq_height)
    seq_width = 1242
    seq_height = 375

    gt_txt = osp.join(seq_root, seq)  # 读取GT文件
    #print(gt_txt)  #打印路径
    #gt = np.loadtxt(gt_txt, dtype=np.str, delimiter=',')  # 加载成np格式

    gt = np.loadtxt(gt_txt, dtype=np.float64, delimiter=',')  # 加载成np格式
    print(gt)  #打印文本内容
    print('gt.T')
    print(gt.T) #也是打印文本内容
    idx = np.lexsort(gt.T[:2, :])  # 优先按照track id排序(对视频帧进行排序, 而后对轨迹ID进行排序)
    # print(idx)
    gt = gt[idx, :]

    tr_ids = set(gt[:, 1])
    print("%d track ids in seq %s" % (len(tr_ids), seq))
    total_track_id_num += len(tr_ids)  # track id统计数量如何正确计算？

    seq_label_root = osp.join(label_root, seq, 'img1')
    mkdirs(seq_label_root)

    # 读取GT数据的每一行(一行即一条数据)
    # for fid, tid, x, y, w, h, mark, cls, vis_ratio in gt:
    for fid, tid, type, truncated, occluded, alpha, \
        bbox_left, bbox_top, bbox_right ,bbox_bottom ,_,_,_,_,_,_,_ in gt:
        #height, width, length , location_x,location_y,location_z , rotation_y in gt:
        # frame_id, track_id, top, left, width, height, mark, class, visibility ratio
        #if cls != 3:  # 我们需要Car的标注数据
        if type != 3:  # 我们需要Car的标注数据
        #flag =(type == 3 or type == 6 or type == 7)  #只要一个符合要求就是真的
        #print("flag:")
        #print(flag)

        #if flag==False:  # 我们需要Car Van Truck的标注数据
            continue

        # if mark == 0:  # mark为0时忽略(不在当前帧的考虑范围)
        #     continue

        # if vis_ratio <= 0.2:
        #     continue

        fid = int(fid)
        tid = int(tid)

        # 判断是否是同一个track, 记录上一个track和当前track
        if not tid == tid_last:  # not 的优先级比 == 高
            tid_curr += 1
            tid_last = tid
        #由于kitti标签与训练标签参数有点不同 需要自己计算 x y w h
        w=float(bbox_right-bbox_left)
        h=float(bbox_bottom-bbox_top)
        x=int(bbox_left+0.5)
        y=int(bbox_top+0.5)

        # bbox中心点坐标
        x += w / 2
        y += h / 2


        # 网label中写入track id, bbox中心点坐标和宽高(归一化到0~1)
        # 第一列的0是默认只对一种类别进行多目标检测跟踪(0是类别)
        label_str = '0 {:d} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(
            tid_curr,
            x / seq_width,   # center_x
            y / seq_height,  # center_y
            w / seq_width,   # bbox_w
            h / seq_height)  # bbox_h
        # print(label_str.strip())

        label_f_path = osp.join(seq_label_root, '{:06d}.txt'.format(fid))
        with open(label_f_path, 'a') as f:  # 以追加的方式添加每一帧的label
            f.write(label_str)

print("Total %d track ids in this dataset" % total_track_id_num)
print('Done')