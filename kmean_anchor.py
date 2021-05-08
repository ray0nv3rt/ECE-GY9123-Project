import numpy as np
import xml.etree.ElementTree as ET
import glob
import random
import os


def cas_iou(box, cluster):
    # print(box)
    # print(cluster)
    x = np.minimum(cluster[:, 0], box[0])
    y = np.minimum(cluster[:, 1], box[1])

    intersection = x * y
    area1 = box[0] * box[1]

    area2 = cluster[:, 0] * cluster[:, 1]
    iou = intersection / (area1 + area2 - intersection)

    return iou


def avg_iou(box, cluster):
    return np.mean([np.max(cas_iou(box[i], cluster)) for i in range(box.shape[0])])


def kmeans(box, k):
    # 取出一共有多少框
    row = box.shape[0]

    # 每个框各个点的位置
    distance = np.empty((row, k))

    # 最后的聚类位置
    last_clu = np.zeros((row,))

    np.random.seed()

    # 随机选5个当聚类中心
    cluster = box[np.random.choice(row, k, replace=False)]
    # cluster = random.sample(row, k)
    while True:
        # 计算每一行距离五个点的iou情况。
        for i in range(row):
            distance[i] = 1 - cas_iou(box[i], cluster)

        # 取出最小点
        near = np.argmin(distance, axis=1)

        if (last_clu == near).all():
            break

        # 求每一个类的中位点
        for j in range(k):
            cluster[j] = np.median(
                box[near == j], axis=0)

        last_clu = near

    return cluster


def load_data():
    data = []
    # aggregate all lengths and weights
    for video_i in range(0, 21):
        filePath = r'D://NYU//2021_Spring//ECE9123//Project//data//label_vehicle//' + str(video_i).zfill(4)

        files = os.listdir(filePath)
        for file in files:
            path = filePath + "//" + file
            # print(path)
            with open(path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    data.append([float(line.split()[4]), float(line.split()[5])])
    return np.array(data)


if __name__ == '__main__':
    # 运行该程序会计算'./VOCdevkit/VOC2007/Annotations'的xml
    # 会生成yolo_anchors.txt
    SIZE = np.array([1248, 384])
    anchors_num = 12
    # 载入数据集，可以使用VOC的xml

    # 载入所有的xml
    # 存储格式为转化为比例后的width,height
    data = load_data()
    print(data)

    # 使用k聚类算法
    out = kmeans(data, anchors_num)
    out = out[np.argsort(out[:, 0])]
    print('acc:{:.2f}%'.format(avg_iou(data, out) * 100))
    print('out')
    print(out)
    print('anchor')
    print(out * SIZE)
    data = out * SIZE
    f = open("yolo_anchors.txt", 'w')
    row = np.shape(data)[0]
    for i in range(row):
        if i == 0:
            x_y = "%d,%d" % (data[i][0], data[i][1])
        else:
            x_y = ", %d,%d" % (data[i][0], data[i][1])
        f.write(x_y)
    f.close()