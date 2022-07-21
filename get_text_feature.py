from transformers import BertTokenizer, BertModel
import os
import pandas as pd
import torch
import pickle

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

def get_label_list(file_name, img_name, label_col):
    csv_file_path = os.path.join(os.getcwd(), file_name)
    df = pd.read_csv(csv_file_path)
    img_names = df[img_name].to_list()
    labels = df[label_col].to_list()
    return labels, img_names

labelFile = 'image_labeling_0720.csv'
colLabel = 'label_eng'
imgName = 'file_name'

listLabel, listImgName = get_label_list(labelFile, imgName, colLabel)
# output_list = []
output_dict = {}

for label, imgName in zip(listLabel, listImgName):
    encoded_input = tokenizer(label, return_tensors='pt')
    output = model(**encoded_input).pooler_output
    # output_list.append(output)
    output_dict[f'{imgName:06d}'] = output

with open('./bg_text_feat.pkl', 'wb') as fid1:
    pickle.dump(output_dict, fid1)
