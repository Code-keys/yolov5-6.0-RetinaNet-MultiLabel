
## <div align="center"><a href="https://xiaoxiaochenxu.top">YOLOv5-v6.0-RetinaNet-MultiLabel<br></a></div>
## <div align="center">Author：<a href="https://github.com/Code-keys/yolov5-6.0-RetinaNet-MultiClass">Code-keys<br></a></div>

<details open>
<summary>Introduction</summary>
<p>
This project :  yolov5-6.0-RetinaNet-MultiLabel 🚀 is a project based on <a href="https://github.com/ultralytics/yolov5">Ultralytics yolov5-v6.0 </a> for detection-framework for multiLabel-detection： <br>
multiLabel-detection：  a bbox contain two or more classes-Info ,such as contain a classname and a degree <br>
</p>
</details>


<details open>
<summary>Write before</summary>

	Merge the Labels to one can also complete your task ( class of M ✖️ N )

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
<summary>VOC datasets-prepare </summary>
Put at the datasets folder{ images/ 、Annotations/ } 

The Annotations should be initialized as follows：

	<object>
		<name>WarShip</name>
		<direction>0</direction>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>

    <object>
		<name>ConmmonShip</name>
		<direction>7</direction>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object>

    <object>
		<name>WarShip</name>
		<direction>4</direction>
		<bndbox>
			<xmin>590</xmin>
			<ymin>119</ymin>
			<xmax>1896</xmax>
			<ymax>1017</ymax>
		</bndbox>
	</object> 
	 

Then split the datasets:
``` bash
	cd datasets/
	mkdir MergedLabels && ln -s images MergedLabels/images
	mkdir MultiLabels && ln -s images MultiLabels/images
	
	python ../split-datasets.py  
```

<details open>
<summary>datasets-convert-for-train</summary>

\<class-id> \<x-center> \<y-center> \<w> \<h> \<other-label-id>：

The labels can be converted as follows ( append a tail behind the yolo-format-line )： 

``` bash
	cd datasets/MergedLabels && mkdir labels
	vim ../voc2myYOLO.py ( Define something ) && python ../voc2myYOLO.py
```
MultiLabels/labels/000000.txt ：  
``` bash
    0 0.255859375 0.6736111111111112 0.13046875 0.47500000000000003 0
    1 0.361328125 0.6777777777777778 0.11484375000000001 0.430555555 3
    1 0.361328125 0.6777777777777778 0.11484375000000001 0.430555555 2
    0 0.432421875 0.6895833333333333 0.08203125 0.37083333333333335 5
    1 0.6957031250000001 0.7152777777777778 0.12578125 0.35833333333333334 7 
```  
</details>

<details open>
<summary>datasets-for-val&test</summary>
  
// merged-class-id : tree children-node
 
\<merged-class-id> \<x-center> \<y-center> \<w> \<h> ：

The images && the datasets-split must be same to corresponding the train-datasets 

The Datasets-labels can be convert as following
``` bash
	cd datasets/MergedLabels && mkdir labels
	vim ../voc2myYOLO.py ( Define something ) && python ../voc2myYOLO.py
```
MergedLabels/labels/000000.txt ： 

    0 0.255859375 0.6736111111111112 0.13046875 0.47500000000000003 
    4 0.361328125 0.6777777777777778 0.11484375000000001 0.4305555555555556  
    11 0.432421875 0.6895833333333333 0.08203125 0.37083333333333335  
    15 0.6957031250000001 0.7152777777777778 0.12578125 0.35833333333333334  
    6 0.6957031250000001 0.7152777777777778 0.12578125 0.35833333333333334  
 
</details>


<details open>
<summary>train</summary> 
Train with ours YOLOv5   

```python 
# datasets.yaml
train: /home/xxx/xxx/dateset/train.txt #  train-format :  yolo-format append a other-id
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
xxx@xxx:~/xxx/yolov5-6.0$  python val_merged.py --weights outputs/yolov5s/weights/best.pt --data your-datasets.yaml
```
</details>


<details open>
<summary>FootStep of Project-Modify</summary> 

###  Abstract

1.	数据集 划分 split   train.txt   et al     -> mergedLabel/images   -> MultiLabels/images 
2.	标签转换     MultiLabels 型(仅用于 train)  +  mergedLabel型 (仅用于 eval-test)
3.	datasets.py：

	verify_image_label(args): ->  assert ...

	class LoadImagesAndLabels ->  __getitem__ ↓

	torch.zeros((nl, 7))  # datasets：Label-format  ( bs class  x y w h other   )

5.	yolo.py 
	
	Detect : 双头：nc nc1 ；适配

6.	val-merged.py
		输出转换后 与 merged 类进行对比:

        # re-assign by class  ( using multiply direct )
        out_val = torch.cat( [ out[..., 0:5] ,out[..., 7:], out[..., 7:] ] , dim=-1 )
        out_val[:, :, 5:13 ] *= (out[:, :, 5:6].repeat(1, 1, 8) )
        out_val[:, :, 13: ]  *= (out[:, :, 6:7].repeat(1, 1, 8) )

7.	Loss.py ->	ComputeLoss  
	
	\#  added BCEcls   
	\#  Define criteria     
	\#  added  a BCEWithLogitsLoss      
	\#  added a FocalLoss ( better ) Focal loss  : FocalLoss(BCEdeg, g)  

	\#  \_\_call__  modify as the lcls  
	Classification &&  other  同
	t = torch.full_like(ps[:, self.nc+5: ], self.cn, device=device) 
						t[range(n), tdeg[i]] = self.cp
						ldeg += self.BCEdeg(ps[:, self.nc+5: ], t)  # BCE 

	
	\# Loss: build_targets  

</details>


<details open>
<summary> Thanks </summary> 
 
 	@ yolov5 for base
	@ deast@hdu.edu.cn for the data&labels
 
</details>
