# API 文档

## 如何启动 web 和 Reset API 服务

本框架使用前后端分离，所以要分别启动前端的页面和后端的 web 服务

### 启动前端页面

前端使用纯前端技术，不需要后端之前就可以运行

运行方式：

1. 直接使用浏览器打开\*.html
2. 使用 Apache http service，使用这种方式只需要修改 apache 服务器的配置文件./conf/httpd.conf 中的 DocumentRoot 和 Directory，将其修改为 Chinese-Annotator\chi_annotator\webui\static。然后重启 httpd 服务器，直接访问 localhost 即可

### 后端服务的启动

后端使用 Python 的 django，所以需要安装必要的包，所需要的依赖包参见项目目录中的 requirements.txt

1. 将/webui export 到 PYTHONPATH
2. 运行 python ca.py

## API 接口说明

/api/load_local_dataset

支持 post 和 get 请求
参数：filepath 本地文件的绝对路径

功能： 将本地的 data 文件中的内容存入 MongoDB

/api/upload_remote_file
仅支持 post 请求
参数：上传的 file 文件

功能：解析上次的 data 文件，并将其内容存入 MongoDB

/api/export_data
仅支持 get 请求
参数：无

功能：将 MongoDB 中的数据，导出到本地 ../../data/files 文件夹的 annotation_data.json 文件中
