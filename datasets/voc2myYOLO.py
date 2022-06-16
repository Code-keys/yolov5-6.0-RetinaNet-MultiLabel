import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

yaml = {}
yaml['names'] = [   "WarShip",  "CommonShip"   ] # define the 1st Labels by yourself    
yaml['others'] = [  "0", "1",  "2", "3",  "4", "5",  "6", "7" ] # define the 2nd Labels  by yourself   

def convert_label(path, image_id):
    def convert_box(size, box):
        dw, dh = 1. / size[0], 1. / size[1]
        x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
        return x * dw, y * dh, w * dw, h * dh

    in_file = open(f"{path}/../Annotations/{image_id}.xml")
    out_file = open(f"{path}/labels/{image_id}.txt", 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text           # CHANGEQ BY YOUR   LABEL
        other = obj.find('direction').text    # CHANGEQ BY YOUR   LABEL
        if cls not in yaml['names']: 
            yaml['names'].append( cls )
        if other not in yaml['others']:
            yaml['others'].append( other )
        if cls in yaml['names'] and not int(obj.find('difficult').text) == 1:
            xmlbox = obj.find('bndbox')
            bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])

            cls_id = yaml['names'].index(cls)       # class id
            other_id = yaml['others'].index(other)  # other-labels id

            out_file.write(" ".join([str(a) for a in (cls_id , *bb, other_id)]) + '\n')



if __name__ == '__main__':

    VOCRoot = os.getcwd()
    try:
        os.mkdir(VOCRoot + "/labels")
    except:
        pass # "rm -rf VOCRoot + \"/labels/*\""
    for xml in tqdm( os.listdir( VOCRoot + '/../Annotations/' ) ):
        convert_label( VOCRoot, xml.split(".")[0] )
    print( yaml["names"] ) 
    print( yaml["others"] )