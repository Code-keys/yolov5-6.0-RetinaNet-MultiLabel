cd /home/gy/NSD/yolov5-6.0 && export Use_Double_Head=1 &&nohup python train.py \
--weights '' \
--device 3 \
--cfg  /home/gy/NSD/yolov5-6.0/outputs/yolov5s.yaml \
>  /home/gy/NSD/yolov5-6.0/outputs/yolov5s.out &