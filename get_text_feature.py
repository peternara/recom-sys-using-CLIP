from transformers import BertTokenizer, BertModel
import os
import pandas as pd
import pickle
import time
from eval import img2text_CLIP

import datetime
import logging
import pytz

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

labelFile = 'image_labeling_0720.csv'
colLabel = 'label_eng'
imgName = 'file_name'

test_dict = {'a':1}

# input: csv file with image name and label
# returns pickle file of dictionary of (key: img file name, value: text features)
def caption2feat(csv_fName, img_fName, label_col, pkl_fName):
    csv_file_path = os.path.join(os.getcwd(), csv_fName)
    df = pd.read_csv(csv_file_path)
    img_names = df[img_fName].to_list()
    labels = df[label_col].to_list()
    
    output_dict = {}
    
    for label, imgName in zip(labels, img_names):
        encoded_input = tokenizer(label, return_tensors='pt')
        output = model(**encoded_input).pooler_output
        # output_list.append(output)
        output_dict[f'{imgName:06d}'] = output
    
    pkl_fName = pkl_fName + '.pkl'
    
    with open(pkl_fName, 'wb') as fid1:
        pickle.dump(output_dict, fid1)
    return pkl_fName

img_extension = ['.png', '.jpg']
bg_asset_path = './background_asset/JHS/'
nCaption = 5

label_bg_asset = {'file name': []}
for n in range(nCaption):
    label_bg_asset['label_' + str(n+1)] = []

class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)
        # Change datetime's timezone
        return dt.astimezone(pytz.timezone('Asia/Seoul'))
    
    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

# Not working...
dt = datetime.datetime.now() + datetime.timedelta(hours=9)
ts = datetime.datetime.timestamp(dt)
logging.Formatter.converter(ts)


# datetime.datetime.now(pytz.timezone('Asia/Seoul')).timetuple()
# time.localtime
# datetime.datetime.now(pytz.timezone('Asia/Seoul'))
logging.basicConfig()
customLogger = logging.getLogger(__name__)
customLogger.setLevel(logging.INFO)
f_handler = logging.FileHandler('generate_caption_bg_JHS.log')
f_handler.setFormatter(logging.Formatter('%(message)s %(asctime+datetime.timedelta(hours=9))s'))
# handler -> setLevel as well? 
f_handler.setLevel(logging.INFO)
customLogger.addHandler(f_handler)
customLogger.info(f'Initiated at:')

cnt_file = 0
for (root, dirs, files) in os.walk(bg_asset_path):
    if len(files) > 0: 
        for file_name in files:
            file_path = os.path.abspath(os.path.join(root, file_name))
            rel_file_path = os.path.join(root, file_name)
            label_list = img2text_CLIP(file_path)[:nCaption]
            cnt_file += 1
            
            label_bg_asset['file name'].append(rel_file_path)
            for n in range(nCaption):
                label_bg_asset['label_'+str(n+1)].append(label_list[n])
            
            if cnt_file % 10 == 0:
                rel_fPath = os.path.join(*rel_file_path.split('/')[2:])
                customLogger.info(f'{cnt_file}th caption of {rel_fPath} is created at:')
            
            
df = pd.DataFrame(label_bg_asset)

df.to_csv('label_bg_asset.csv', index=False)