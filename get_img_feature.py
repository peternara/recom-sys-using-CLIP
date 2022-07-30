from ImageCaptioning_def import get_img_feats
import clip
import torch
import cv2
import os
import numpy as np

clip_version = "ViT-B/16"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
#Must set jit=False for training
# model = torch.load("model.pt", map_location="cpu")
model, preprocess = clip.load(clip_version, device=device, jit=False)

img_ext = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']
img_dir = './background_asset/'
img_feats_list = []

# FINAL len(img_feats_list) = 449
for (root, dir, files) in os.walk(img_dir):
    if len(files) > 0: 
        for file_name in files:
            if os.path.splitext(file_name)[1] in img_ext:
                file_path = os.path.abspath(os.path.join(root, file_name))
                image = cv2.imread(file_path)
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # , cv2.COLOR_BGR2RGB
                img_feats = get_img_feats(model, preprocess, img)
                img_feats_list.append(img_feats)

np.save('img_feats_list_512.npy', img_feats_list)