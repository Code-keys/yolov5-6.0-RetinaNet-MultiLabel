from utils.autoanchor import kmean_anchors  
from utils.datasets import create_dataloader, LoadImagesAndLabels
import tqdm


# kmean_anchors(dataset='/home/gy/NSD/yolov5-6.0/Rship.yaml', n=9, img_size=640, thr=4.0, gen=6000, verbose=True ) 

dataset = LoadImagesAndLabels( "/home/gy/NSD/yolov5-6.0/datasets/images_train.txt" , 640, 8 ) 

for i, (imgs, targets, paths, _)  in tqdm.tqdm(enumerate(dataset)):
    print(i, " ",  targets.size() )