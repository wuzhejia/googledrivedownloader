from flask import Flask, render_template, request, send_file
import gdown

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # 获取表单中的 Google Drive 共享链接
    drive_link = request.form['drive_link']

    # 从 Google Drive 下载文件到服务器
    output_file = 'downloaded_file'
    gdown.download(drive_link, output_file, quiet=False)

    # 返回一个页面，包含文件的下载链接
    return render_template('download.html', file_name=output_file)

@app.route('/get_file/<file_name>')
def get_file(file_name):
    # 提供文件的下载链接
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    # Make the app accessible from any IP on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)