# Google Drive Downloader 部署文档

## 目的

解决在 Google Drive 上下载大体积文件因为 Google Drive 1 小时的安全时效设置而失败的问题。

## 系统环境

### 服务器

- 操作系统: Alibaba Cloud Linux 2.1903 LTS 64位
- Python 版本: 3.6.8
- 使用 pip 安装的库: gdown, flask, gunicorn
- 额外工具: ossutil, SSL 版本大于 1.1.1

### 阿里云 OSS

- 两个 Bucket，一个在上海，一个在韩国
- 配置跨区域复制，将韩国的 Bucket 内容实时同步至上海 Bucket

## 部署步骤

1. **环境准备**

   确保服务器上已经安装了必要的工具和库，包括 Python 3.6.8、pip、gdown、flask、gunicorn、ossutil。

   ```bash
   # 示例：安装 gdown, flask, gunicorn
   pip install gdown flask gunicorn
   ```

   [ossutil 安装参考阿里云 OSS 文档](https://help.aliyun.com/document_detail/120075.html)

2. **OSS 设置**

   - 在阿里云 OSS 上分别创建上海和韩国的 Bucket。
   - 配置跨区域复制，确保韩国 Bucket 的内容实时同步至上海 Bucket。

3. **代码部署**

   - 将 `prod` 文件夹上传至服务器。

   - 在服务器上运行 Gunicorn 启动 Flask 应用。

     ```bash
     gunicorn -w 4 -b 0.0.0.0:5000 -D gd:app --error-logfile gunicorn-error.log --access-logfile gunicorn-access.log
     ```

4. **监控日志**

   - 监控 Gunicorn 日志以确保应用正常运行。

     ```bash
     # 示例：查看错误日志
     tail -f gunicorn-error.log
     ```

     ```bash
     # 示例：查看访问日志
     tail -f gunicorn-access.log
     ```

## 注意事项

- 请确保 SSL 版本大于 1.1.1 以满足 Google Drive 的要求。
- 在部署过程中确保服务器和 OSS 的配置准确，特别是跨区域复制设置。
- 建议在部署前仔细阅读阿里云 OSS 文档和 Google Drive API 文档，确保对应用程序的权限和安全性有清晰的了解。