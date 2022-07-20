# Modified by Sehyun Kim, 2022-07-20(July 20th, 2022), @RebuilderAI, Seoul, South Korea

from flask import Flask, request, render_template
import os
import datetime
import time
from eval import img2text_CLIP
from googletrans import Translator

abs_path = os.path.dirname(os.path.abspath(__file__))
# In the current directory 'templates' directory has html templates(index.html, etc.)
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

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
        # Create 'images' folder in the 'static' folder and save the uploaded images in it
        img_save_dir = os.path.join(save_dir, 'images')
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
            os.mkdir(img_save_dir)
        
        requests = request.files.getlist('images')
        filePathList = []
        # Relative path of the uploaded images is needed to display(through render_template() ) them in the browser
        relFilePathList = []
        
        for idx, req in enumerate(requests):
            relFilePath = os.path.join(stream_id, 'images')
            relFilePath = os.path.join(relFilePath, f"{idx:05d}.png")
            filePath = os.path.join(img_save_dir, f"{idx:05d}.png")
            req.save(filePath)
            relFilePathList.append(relFilePath)
            filePathList.append(filePath)

        begin_time = time.time()
        # img2text_CLIP takes an image file(path) and returns a caption(text) that describes input image the best
        caption_orig = img2text_CLIP(filePathList[0])
        end_time = time.time()
        app.logger.info(end_time - begin_time)
        
        translator = Translator()
        caption_trans = translator.translate(caption_orig, src='en', dest='ko').text
        exec_time = begin_time - end_time
        
        return render_template('result.html', filePath=relFilePathList[0],caption_eng=caption_orig,
                               caption_ko=caption_trans, time=round(exec_time, 2))

    except Exception as e:
        print(e)
        return render_template('fail.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9081, debug=False)