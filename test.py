# Modified by Sehyun Kim, 2022-07-29(July 29th, 2022), @RebuilderAI, Seoul, South Korea

import clip
import cv2
import torch
from eval_keywords import kwords_imgFeat_CLIP
from ImageCaptioning_def import get_img_feats

clip_version = "ViT-B/16"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
#Must set jit=False for training
# model = torch.load("model.pt", map_location="cpu")
model, preprocess = clip.load(clip_version, device=device, jit=False)

# img_path = 'test_background_img/museum2.jpg'
img_path = 'test_background_img/bright_studio1.jpg'
moods, colors, places, objs, img_feat = kwords_imgFeat_CLIP(img_path)

for i in range(3):
    print(moods[i], colors[i], places[i], objs[i], sep='\n')
# image = cv2.imread(file_path)
# img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # , cv2.COLOR_BGR2RGB
# img_feats = get_img_feats(model, preprocess, img)
