from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import humanize

app = Flask(__name__)

# 设置上传文件夹路径
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB

@app.route('/')
def index():
    return render_template('files.html')

@app.route('/api/files')
def list_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        stats = os.stat(path)
        
        file_info = {
            'name': filename,
            'size': humanize.naturalsize(stats.st_size),
            'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
        }
        files.append(file_info)
    
    return jsonify(files)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有选择文件', 400
    
    file = request.files['file']
    if file.filename == '':
        return '文件名为空', 400
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return '文件上传成功', 200

if __name__ == '__main__':
    app.run(debug=True)