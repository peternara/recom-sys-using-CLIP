# Created by Sehyun Kim, 2022-07-20(July 20th, 2022), @RebuilderAI, Seoul, South Korea

from transformers import BertTokenizer, BertModel
import os
from eval import img2text_CLIP
from torch import nn
import pickle
import cv2
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

test_img_path = './test_images'
caption = img2text_CLIP(os.path.join(test_img_path, 'cosmetics.jpg'))

encoded_input = tokenizer(caption, return_tensors='pt')
output = model(**encoded_input).pooler_output

cos_sim = nn.CosineSimilarity(dim=1, eps=1e-6)

with open("bg_text_feat.pkl", "rb") as fp1:
    label_text = pickle.load(fp1)
    
score_list = []

for fileName, label in label_text.items():
    score_list.append((cos_sim(output, label), fileName))

maxScoreFileName = max(score_list)[1]

file_path = os.path.join(test_img_path, maxScoreFileName)
cv2.imshow(file_path)