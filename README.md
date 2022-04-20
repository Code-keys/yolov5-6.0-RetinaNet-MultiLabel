
## <div align="center"><a href="https://xiaoxiaochenxu.top">YOLOv5-v6.0-RetinaNet-MultiLabel<br></a></div>
## <div align="center">Author：<a href="https://github.com/Code-keys/yolov5-6.0-RetinaNet-MultiClass">Code-keys<br></a></div>

<details open>
<summary>Introduction</summary>
<p>
This project :  yolov5-6.0-RetinaNet-MultiClass 🚀 is a project based on <a href="https://github.com/ultralytics/yolov5">Ultralytics yolov5-v6.0 </a> for detection-framework for multiLabel-detection： <br>
multiLabel-detection：  a bbox contain two or more classes-Info ,such as contain a classname and a degree <br>
</p>
</details>



## <div align="center">Quick Start Examples</div>

<details open>
<summary>Install</summary>

[**Python>=3.6.0**](https://www.python.org/) is required with all
[requirements.txt](https://github.com/ultralytics/yolov5/blob/master/requirements.txt) installed including
[**PyTorch>=1.7**](https://pytorch.org/get-started/locally/):
<!-- $ sudo apt update && apt install -y libgl1-mesa-glx libsm6 libxext6 libxrender-dev -->

```bash
$ git clone https://github.com/Code-keys/yolov5-6.0-RetinaNet-MultiClass
$ cd yolov5-6.0-RetinaNet-MultiClass
$ pip install -r requirements.txt
```

</details>

<details open>
<summary>datasets-train</summary>

The Datasets-Annotations should be initialized as follows： 

	<object>
		<name>cat</name>
		<sex>male</sex>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>	

    <object>
		<name>dog</name>
		<sex>female</sex>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>


The Datasets-labels can be code as follows ( like yolo-format )： 

    ...
    sex =  obj.find('sex').text  
    sex = int( all_sexes.index(sex) )  
    cls = obj.find('name').text
    cls_name_id = int( all_classes.index(cls) )   
    xmlbox = obj.find('bndbox')
    xywh = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])  
    out_file.write(" ".join([str(a) for a in (cls_name_id ,*xywh, sex)]) + '\n')

labels/000000.txt ： \<class-id> \<x-center> \<y-center> \<w> \<h> \<sex-id>：

    0 0.255859375 0.6736111111111112 0.13046875 0.47500000000000003 1
    2 0.361328125 0.6777777777777778 0.11484375000000001 0.4305555555555556 0
    3 0.432421875 0.6895833333333333 0.08203125 0.37083333333333335 1
    1 0.6957031250000001 0.7152777777777778 0.12578125 0.35833333333333334 0


</details>

<details open>
<summary>datasets-val</summary>

The Datasets-Annotations should be initialized as follows： 

	<object>
		<name>cat</name>
		<sex>male</sex>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>	

    <object>
		<name>dog</name>
		<sex>female</sex>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>


The Datasets-labels can be code as follows ( like yolo-format )： 

    ...
    sex =  obj.find('sex').text  
    sex = int( all_sexes.index(sex) )  
    cls = obj.find('name').text
    cls_name_id = int( all_classes.index(cls) )   

    new_cls_id = all_sexes.__len__() * cls_name_id + sex    ###    ####  2*cls+sex

    xmlbox = obj.find('bndbox')
    xywh = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])  
    out_file.write(" ".join([str(a) for a in (new_cls_id ,*xywh, sex)]) + '\n') 

labels/000000.txt ： \<new-class-id> \<x-center> \<y-center> \<w> \<h> ：

    1 0.255859375 0.6736111111111112 0.13046875 0.47500000000000003 
    4 0.361328125 0.6777777777777778 0.11484375000000001 0.4305555555555556  
    7 0.432421875 0.6895833333333333 0.08203125 0.37083333333333335  
    2 0.6957031250000001 0.7152777777777778 0.12578125 0.35833333333333334  
 
</details>

<details open>
<summary>train</summary> 
Train with ours YOLOv5   

```python 
# datasets.yaml
train: /home/xxx/xxx/dateset/train.txt #  train-format :  yolo-format append a sex-id
val: /home/xxx/xxx/dateset/eval.txt  #  val-format : new_cls_id 交叉乘积结果
test: /home/xxx/xxx/dateset/test.txt  # val-format 
``` 
train：
```sh 
xxx@xxx:~/xxx/yolov5-6.0$  export Use_Double_Head=1
xxx@xxx:~/xxx/yolov5-6.0$  python train.py --cfg outputs/yolov5s.yaml --data datasets.yaml 
``` 
</details>



<details open>
<summary>val</summary>
key codes modified as follows:

        out, train_out = model(img, augment=augment)  # inference and training outputs  

        # re-assign by class
        out_val = torch.cat( [ out[..., 0:5] ,out[..., 7:], out[..., 7:] ] , dim=-1 )
        out_val[:, :, 5:13 ] *= (out[:, :, 5:6].repeat(1, 1, 8) )
        out_val[:, :, 13: ]  *= (out[:, :, 6:7].repeat(1, 1, 8) )
val：
```python
xxx@xxx:~/xxx/yolov5-6.0$  export Use_Double_Head=1
xxx@xxx:~/xxx/yolov5-6.0$  python val_16.py --weights outputs/yolov5s/weights/best.pt --data datasets.yaml 
```
</details>
