import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

yaml = {}
yaml['names'] = [   "WarShip",  "CommonShip"   ] # define the 1st Labels by yourself    
yaml['others'] = [  "0", "1",  "2", "3",  "4", "5",  "6", "7" ] # define the 2nd Labels  by yourself   

def convertMerge_labels(path, image_id):
    def convert_box(size, box):
        dw, dh = 1. / size[0], 1. / size[1]
        x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
        return x * dw, y * dh, w * dw, h * dh

    in_file = open(f"{path}/../Annotations/{image_id}.xml")
    out_file = open(f"{path}//labels/{image_id}.txt", 'w')
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
 
            c0 = yaml['names'].index(cls)
            lenc0 =  yaml['names'].__len__()
            c1 = yaml['others'].index(other)
            lenc1 =  yaml['others'].__len__() 

            # 树形结构 下的 叶子节点 id
            cls_id =   c1 + c0 * lenc0 

            out_file.write(" ".join([str(a) for a in (cls_id,  *bb)]) + '\n')  

            """ 
            ↓↓↓↓↓↓↓↓↓↓↓↓ MultiLabels of three Type of label  or more  ↓↓↓↓↓↓↓
            c0 = yaml['names'].index(cls)
            lenc0 =  yaml['names'].__len__()
            c1 = yaml['other'].index(other)
            lenc1 =  yaml['others'].__len__()
            c3 = yaml['another'].index(colors) 
            lenc3 =  yaml['another'].__len__()

            # 树形结构 下的 叶子节点 id
            cls_id =   c1 + c0 * lenc0  + c1 * lenc2 * lenc3 """



if __name__ == '__main__':

    VOCRoot = './' # (your-project)/datasets/MergedLabels
    try:
        os.mkdir(VOCRoot + "/labels")
    except:
        pass # "rm -rf VOCRoot + \"/labels/*\""
    for xml in tqdm( os.listdir( VOCRoot + '/../Annotations/' ) ):
        convertMerge_labels( VOCRoot, xml.split(".")[0] )

    print( yaml["names"] ) 
    print( yaml["others"] )