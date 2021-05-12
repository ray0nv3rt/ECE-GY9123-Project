import os

# train dir
#image_folder = '/scratch/zc2237/Towards-Realtime-MOT/dataset/KITTI/train/images'
# test dir
image_folder = '/scratch/zc2237/Towards-Realtime-MOT/dataset/KITTI/test/images'
folders = os.listdir(image_folder)
#train_file = open('/scratch/zc2237/Towards-Realtime-MOT/data/KITTI-car.train', 'w')
test_file = open('/scratch/zc2237/Towards-Realtime-MOT/data/KITTI-car.test', 'w')

#print(image_folder)

for f in folders:
    imgs = os.listdir(image_folder + '/' + f)
    for img in imgs:
        save_str = image_folder + "/" + f + '/' + img + '\n'
        print(save_str)
        #train_file.write(save_str)
        test_file.write(save_str)

#train_file.close()


#imgs = os.listdir(image_folder)
#for img in imgs:
#    save_str = image_folder + '/' + img + '\n'
#    print(save_str)
#    test_file.write(save_str)

test_file.close()
