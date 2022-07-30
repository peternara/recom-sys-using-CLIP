# Modified by Sehyun Kim, 2022-07-20(July 20th, 2022), @RebuilderAI, Seoul, South Korea

from flask import Flask, request, render_template
import os
import datetime
import time
from transformers import BertTokenizer, BertModel
from eval import img2text_CLIP
import pickle
from torch import nn
from googletrans import Translator

abs_path = os.path.dirname(os.path.abspath(__file__))
# In the current directory 'templates' directory has html templates(index.html, etc.)
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# tokenizer and bert_model embeds caption texts into vectors(text feature vectors)
# Cosine similarity can be calculated from a pair of text feature vectors
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained("bert-base-uncased")
translator = Translator()
cos_similarity = nn.CosineSimilarity(dim=1, eps=1e-6)
nCaption = 5

imgPath = os.path.join(abs_path, 'static')
imgPath = os.path.join(imgPath, 'instagram_img')

with open("bg_text_feat.pkl", "rb") as fd:
    bg_text_feat = pickle.load(fd)

# Returns homepage
@app.route('/', methods=['GET'])
def home(project_name='', img_paths=''):
    return render_template("home.html", project_name=project_name, img_paths=img_paths)

# If user uploads an image, this function is called
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Create 'static' folder in the current directory if it does not exist
        stream_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        save_dir = os.path.join(abs_path, 'static', stream_id)
        # Create 'images' folder in the 'static' folder if it does not exist
        img_save_dir = os.path.join(save_dir, 'images')
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
            os.mkdir(img_save_dir)
        
        requests = request.files.getlist('images')
        filePathList = []
        # Relative path of the uploaded images is needed to display(through render_template() ) them in the browser
        relFilePathList = []
        
        # Save uploaded image in the 'images' folder
        for idx, req in enumerate(requests):
            relFilePath = os.path.join(stream_id, 'images')
            relFilePath = os.path.join(relFilePath, f"{idx:05d}.png")
            filePath = os.path.join(img_save_dir, f"{idx:05d}.png")
            req.save(filePath)
            relFilePathList.append(relFilePath)
            filePathList.append(filePath)

        # Begin step 1) generating a caption from uploaded image step 2) recommending background asset
        begin_time = time.time()
        # img2text_CLIP takes an image file(path) and returns a caption(text) that describes input image the best
        caption_orig_list = img2text_CLIP(filePathList[0])
        rec_img_fName_list = []
        
        for i in range(nCaption):
            encoded_input = tokenizer(caption_orig_list[i], return_tensors='pt')
            caption_feat = bert_model(**encoded_input).pooler_output

            sim_score_list = []
            for bg_img_fName, candidate in bg_text_feat.items():
                sim_score_list.append((cos_similarity(caption_feat, candidate), bg_img_fName))
            rec_img_fName = max(sim_score_list)[1]
            rec_img_fName_list.append(rec_img_fName)
        
        # sorted_score_list = sorted(sim_score_list)
        # rec_img_fName = sorted_score_list[0][1]
        
        rel_img_path_list = []
        for i in range(nCaption):
            # rec_img_fName = '000101' imgPath = 'static/instagram_img/'
            rec_img_fPath = os.path.join(imgPath, rec_img_fName_list[i])
            # if img file extension is jpg
            if os.path.isfile(rec_img_fPath + '.jpg'):
                fName_with_ext = rec_img_fName_list[i] + '.jpg'
            # if img file extension is png
            elif os.path.isfile(rec_img_fPath + '.png'):
                fName_with_ext = rec_img_fName_list[i] + '.png'
                
            rel_img_path_list.append(os.path.join('instagram_img', fName_with_ext) )
        
        caption_orig_best = caption_orig_list[0]
        caption_trans_best = translator.translate(caption_orig_best, src='en', dest='ko').text
        
        end_time = time.time()
        exec_time = end_time - begin_time
        
        return render_template('result.html', num_caption=nCaption, filePath=relFilePathList[0], caption_eng=caption_orig_best,
                               caption_ko=caption_trans_best, recommended_imgs=rel_img_path_list, time=round(exec_time, 2))

    except Exception as e:
        print(e)
        return render_template('fail.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9080, debug=False)