# -*- coding: utf-8 -*-
"""ComputerVision_Cards.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19-1OikBLBF0NPpzx1L2vqk79GjF6Lq7C
"""

# Commented out IPython magic to ensure Python compatibility.
# 파이토치 버전의 YOLO 모델 version 5 소스 코드를 다운로드

!git clone https://github.com/ultralytics/yolov5  # clone
# %cd yolov5
!pip install -r requirements.txt  # install

# 로보플로에서 생성한 데이터셋을 다운로드

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="")
project = rf.workspace("").project("")
dataset = project.version(1).download("")

# pre-trained weights

!wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
!ls

# 학습
# 이미지 크기 (640x640),
# 배치 크기 (5장),
# 전체 데이터 반복 횟수 (50번),
# 데이터셋 경로 (data.yaml 파일: 로보플로 자동 생성)

!python train.py --img 640 --batch 5 --epochs 50 --data PokerCard-1/data.yaml --weights yolov5s.pt

# Commented out IPython magic to ensure Python compatibility.
# 학습 추세 확인
# %load_ext tensorboard
# %tensorboard --logdir runs/train

# 평가 단계
!python detect.py --weight runs/train/exp/weights/best.pt --conf 0.1 --source PokerCard-1/test/images

# 평가 결과를 시각화
import glob
from IPython.display import Image, display

for i, imageName in enumerate(glob.glob('runs/detect/exp3/*.jpg')): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

# c++ libtorch 에서 사용하기 위한 포맷으로 변환
!python export.py --weights runs/train/exp/weights/best.pt --include torchscript
!ls runs/train/exp/weights/

# Commented out IPython magic to ensure Python compatibility.
# 학습된 weight 파일을 구글드라이브에 저장
from google.colab import drive
drive.mount('/content/gdrive')
# %cp /content/yolov5/runs/train/exp/weights/best.torchscript /content/gdrive/My\ Drive/yolov5_best.torchscript