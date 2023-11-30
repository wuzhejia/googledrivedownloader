from flask import Flask, render_template, request, send_file
import gdown
import os
import subprocess
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # 获取表单中的 Google Drive 共享链接和用户输入的文件名
    drive_link = request.form['drive_link']
    file_name = request.form['file_name']

    # 提取文件 ID
    file_id = drive_link.split('/')[-2]

    # 设置下载和上传的目录
    download_folder = '/root/prod/download'

    # 如果是文件夹链接，使用 gdown.download_folder 下载整个文件夹
    if '/folders/' in drive_link:
        # 创建一个临时目录
        temp_folder = os.path.join(download_folder, 'temp_folder')
        os.makedirs(temp_folder, exist_ok=True)
        
        # 执行 gdown.download_folder
        gdown.download_folder(drive_link, output=temp_folder, quiet=False)

        # 压缩文件夹
        zip_file_name = f'{file_name}.zip'
        zip_command = f'zip -r {zip_file_name} {temp_folder} && mv {zip_file_name} {download_folder}'
        subprocess.run(zip_command, shell=True)

        # 删除临时目录
        shutil.rmtree(temp_folder)

        # 调用 ossutil64 工具上传压缩后的文件夹
        upload_command = f'ossutil cp {download_folder}/{zip_file_name} oss://googledrive-korea'

        # 执行命令，获取命令执行结果
        result = subprocess.run(upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # 获取上传是否成功的信息
        upload_success = "成功" if result.returncode == 0 else "失败"

        # 返回一个页面，包含上传是否成功的信息
        return render_template('download.html', upload_success=upload_success)
    else:
        # 构建 Google Drive 文件的直接下载链接
        download_url = f'https://drive.google.com/uc?id={file_id}'

        # 从 Google Drive 下载文件到服务器，保存时使用用户输入的文件名
        output_file = os.path.join(download_folder, f'{file_id}.downloaded')
        gdown.download(download_url, output_file, quiet=False)

        # 新的文件名，加上用户输入的文件名
        new_file_name = os.path.join(download_folder, f'{file_name}')

        # 重命名文件，去掉 ".downloaded" 后缀
        os.rename(output_file, new_file_name)

        # 调用 ossutil64 工具上传文件
        upload_command = f'ossutil cp {new_file_name} oss://googledrive-korea'

        # 执行命令，获取命令执行结果
        result = subprocess.run(upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # 获取上传是否成功的信息
        upload_success = "成功" if result.returncode == 0 else "失败"

        # 返回一个页面，包含上传是否成功的信息
        return render_template('download.html', upload_success=upload_success)

@app.route('/get_file/<file_name>')
def get_file(file_name):
    # 提供文件的下载链接
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)