# Modified by Sehyun Kim, July 18th, 2022

BATCH_SIZE = 4
EPOCH = 10

import torch
from torch import optim
import torch.nn as nn
import clip
# import torch.nn.functional as F
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import os
import cv2
# import matplotlib.pyplot as plt
import numpy as np
from profanity_filter import ProfanityFilter
from ImageCaptioning_def import num_params, get_img_feats, get_text_feats, get_nn_text, prompt_llm
import pickle
import pandas as pd
from datetime import date, datetime
import time

# model = torch.load("model.pt", map_location="cpu")

clip_version = "ViT-L/14"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
#Must set jit=False for training
# model = torch.load("model.pt", map_location="cpu")
model, preprocess = clip.load(clip_version, device=device, jit=False)

model.cuda().eval()

# Load scene categories from Places365 and compute their CLIP features.
place_categories = np.loadtxt('./categories_places365.txt', dtype=str)
place_texts = []
for place in place_categories[:, 0]:
    place = place.split('/')[2:]
    if len(place) > 1:
            place = place[1] + ' ' + place[0]
    else:
            place = place[0]
    place = place.replace('_', ' ')
    place_texts.append(place)
place_feats = get_text_feats(model, [f'Photo of a {p}.' for p in place_texts])

if not os.path.exists("./object_texts.pkl"):
    # Load object categories from Tencent ML Images.
    with open('./dictionary_and_semantic_hierarchy.txt') as fid:
        object_categories = fid.readlines()
    object_texts = []
    pf = ProfanityFilter()
    # len(object_categories) = 11166
    for object_text in object_categories[1:]:
        object_text = object_text.strip()
        object_text = object_text.split('\t')[3]
        safe_list = ''
        for variant in object_text.split(','):
            text = variant.strip()
            if pf.is_clean(text):
                safe_list += f'{text}, '
        safe_list = safe_list[:-2]
        if len(safe_list) > 0:
                object_texts.append(safe_list)
            
    object_texts = [o for o in list(set(object_texts)) if o not in place_texts]  # Remove redundant categories.
    object_feats = get_text_feats(model, [f'Photo of a {o}.' for o in object_texts])

    with open('object_texts.pkl', 'wb') as fid1:
        pickle.dump(object_texts, fid1)
    with open('object_feats.pkl', 'wb') as fid2:
        pickle.dump(object_feats, fid2)

else:
    with open("object_feats.pkl", "rb") as fp1:
        object_feats = pickle.load(fp1)
    with open("object_texts.pkl", "rb") as fp2:
        object_texts = pickle.load(fp2)
        
# Zero-shot VLM: Classify image mood
img_moods = ['calm', 'monotonous',  'festive', 'gloomy', 'dreary', 'grotesque', 'cozy', 'hopeful', 
                'hopeless', 'promising', 'horrible', 'scary', 'frightening', 'humorous', 'mysterious', 
                'peaceful', 'romantic', 'solitary', 'urgent', 'tense', 'tragic', 'comic', 'desperate', 
                'dynamic', 'moving', 'touching', 'encouraging', 'heartening', 'depressing', 'discouraging', 
                'disheartening', 'fantastic', 'awesome', 'spectacular', 'stressful', 'lively', 'brisk', 'dull', 
                'boring', 'wearisome', 'tiresome', 'inspiring', 'relaxing', 'nostalgic', 'disgusting', 
                'delightful', 'joyful', 'pleasant', 'merry', 'idle', 'solemn', 'grave', 'annoying', 'irritating', 
                'threatening', 'gorgeous', 'prophetic', 'suspenseful', 'thrilling', 'pastoral', 'pitiful', 
                'magnificent', 'natural']

img_colors = ['White', 'Yellow', 'Blue', 'Red', 'Green', 'Black', 'Brown', 'Beige', 'Azure', 'Ivory', 'Teal', 'Silver', 'Purple', 'Navy blue', 'Pea green', 'Gray', 'Orange', 'Maroon', 'Charcoal', 'Aquamarine', 'Coral', 'Fuchsia', 'Wheat', 'Lime', 'Crimson', 'Khaki', 'Hot pink', 'Magenta', 'Olden', 'Plum', 'Olive', 'Cyan']

obj_topk = 10
num_captions = 5

def test_CLIP(img_path):
    startTime = time.time()

    # Load image
    image = cv2.imread(img_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # , cv2.COLOR_BGR2RGB
    
    img_feats = get_img_feats(model, preprocess, img)
    # plt.imshow(img)
    # plt.show()
    
    img_moods_feats = get_text_feats(model, [f'Mood of the image is {t}.' for t in img_moods])
    sorted_img_moods, img_mood_scores = get_nn_text(img_moods, img_moods_feats, img_feats)
    img_mood = sorted_img_moods[0]

    ### Zero-shot VLM: classify image color
    img_colors_feats = get_text_feats(model, [f'Color of the image background is {t}.' for t in img_colors])
    sorted_img_colors, img_color_scores = get_nn_text(img_colors, img_colors_feats, img_feats)
    img_color = sorted_img_colors[0]

    # Zero-shot VLM: classify places.
    place_topk = 3
    place_feats = get_text_feats(model, [f'Photo of a {p}.' for p in place_texts ])
    sorted_places, places_scores = get_nn_text(place_texts, place_feats, img_feats)

    # Zero-shot VLM: classify objects.
    
    sorted_obj_texts, obj_scores = get_nn_text(object_texts, object_feats, img_feats)
    object_list = ''
    for i in range(obj_topk):
        object_list += f'{sorted_obj_texts[i]}, '
    object_list = object_list[:-2]

    # Zero-shot LM: generate captions.
    prompt = f'''
        I am an intelligent image captioning bot.
        I think there might be a {object_list} in {sorted_places[0]} with a {img_color} {img_mood} background.
        Please recommend a background that goes well with selling this item. What kind of studio, lighting atmosphere, and props would fit?'''
    
    # Using GPT-3, generate image captions
    caption_texts = [prompt_llm(prompt, temperature=0.9) for _ in range(num_captions)]

    # Zero-shot VLM: rank captions
    caption_feats = get_text_feats(model, caption_texts)
    sorted_captions, caption_scores = get_nn_text(caption_texts, caption_feats, img_feats)

    endTime = time.time()
    
    return sorted_captions, endTime - startTime
    
##########################