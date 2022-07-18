from flask import Flask, request, render_template
import os
import datetime
import time
from eval import test_CLIP
from werkzeug.utils import secure_filename

# abs_path = os.path.abspath('./') + '/'
abs_path = os.path.dirname(os.path.abspath(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir) # NOTE: 첫번째!!

@app.route('/', methods=['GET'])
# def home(project_name='', methods=['GET', 'POST'], img_paths=[]):
def home(project_name='', img_paths=''):
    # print('@@', project_name, img_paths)
    return render_template("home.html", project_name=project_name, img_paths=img_paths)


# @app.route('/', methods=['GET', 'POST']) # REST API 구조다!
@app.route('/upload', methods=['POST'])
def upload():
    try:
        stream_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        save_dir = os.path.join(abs_path, 'streams', stream_id)
        files_dir = os.path.join(save_dir, 'files')
        img_save_dir = os.path.join(save_dir, 'images')
        obj_save_dir = os.path.join(save_dir, 'objects')
        
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
            os.mkdir(files_dir)
            os.mkdir(img_save_dir)
            os.mkdir(obj_save_dir)
        
        # file = request.files['images']
        # filename = secure_filename(file.filename)
        # # filepath = os.path.join(img_save_dir, f'00000.png')
        # file.save(img_save_dir, filename)
        # print(img_save_dir)
        # print(filepath)
        
        requests = request.files.getlist('images')
        filelist = []
        
        for idx, req in enumerate(requests):
            filepath = os.path.join(img_save_dir, f"{idx:05d}.png")
            req.save(filepath)
            filelist.append(filepath)
        
        # print(filelist)
        # file = request.files['file']
        # filename = file.filename
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # img_src = url_for('static', filename = 'uploads/' + filename)
        # img_src = filelist[0]

        start_time = time.time()
        print(f'filelist: {filelist[0]}')
        captionList, execTime = test_CLIP(filelist[0])
        
        end_time = time.time()
        app.logger.info(end_time-start_time)
        
        return render_template('index.html', image_file=filelist[0], caption=captionList, time=execTime)
        # return f'{captionList[0]}'


    except Exception as e:
        print(e)
        return "실패입니다"    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9081, debug=True)  # http  # NOTE: 두번쨰!!