import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

yaml = {}
yaml['names'] = []

def convert_label(path, image_id):
    def convert_box(size, box):
        dw, dh = 1. / size[0], 1. / size[1]
        x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
        return x * dw, y * dh, w * dw, h * dh

    in_file = open(f"{path}/Annotations/{image_id}.xml")
    out_file = open(f"{path}/labels/{image_id}.txt", 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        degrees = int(obj.find('direction').text)
        if cls not in yaml['names']:
            yaml['names'].append( cls )
        if cls in yaml['names'] and not int(obj.find('difficult').text) == 1:
            xmlbox = obj.find('bndbox')
            bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])

            cls_id = yaml['names'].index(cls)  # class id
            
            out_file.write(" ".join([str(a) for a in (cls_id ,*bb, degrees)]) + '\n')


import random
def split(full_list,shuffle=True,train=0.55, val=0.25):
    n_total = len(full_list)
    offset = int(n_total * train)
    offset2 = int(n_total * val)
    if n_total==0 or offset<1:
        return [],full_list
    if shuffle:
        random.shuffle(full_list)
    sublist = full_list[:offset]
    with open( "/home/gy/NSD/yolov5-6.1/dateset/train.txt" , "w") as f:
        for ii in sublist:
            f.write( ii+"\n") 

    sublist = full_list[offset: offset+offset2 ] 
    with open( "/home/gy/NSD/yolov5-6.1/dateset/eval.txt" , "w") as f:
        for ii in sublist:
            f.write( ii+"\n") 

    sublist = full_list[ offset+offset2  :] 
    with open( "/home/gy/NSD/yolov5-6.1/dateset/test.txt" , "w") as f:
        for ii in sublist:
            f.write( ii+"\n") 
    print("OK !")
    return  


if __name__ == '__main__':
 
    # VOCRoot = '/home/gy/NSD/yolov5-6.1/dateset'
    # try:
    #     os.mkdir(VOCRoot + "/labels")
    # except:
    #     pass
    # for xml in tqdm( os.listdir( VOCRoot + '/Annotations/' ) ):
    #     convert_label( VOCRoot, xml.split(".")[0] )
    # print( yaml["names"] ) 