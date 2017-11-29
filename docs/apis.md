
#API 文档

## 如何启动web和Reset API 服务
本框架使用前后端分离，所以要分别启动前端的页面和后端的web服务

### 启动前端页面
前端使用纯前端技术，不需要后端之前就可以运行

运行方式：
1. 直接使用浏览器打开*.html
2. 使用Apache http service，使用这种方式只需要修改apache服务器的配置文件./conf/httpd.conf中的DocumentRoot和Directory，将其修改为Chinese-Annotator\chi_annotator\webui\static。然后重启httpd服务器，直接访问localhost即可

### 后端服务的启动
后端使用Python的flask，所以需要安装必要的包，所需要的依赖包参见项目目录中的requirements.txt
1. 将/webui export到PYTHONPATH
2. 运行 python ca.py


## API 接口说明
/load_local_dataset

支持post和get请求
参数：filepath 本地文件的绝对路径

功能： 将本地的data文件中的内容存入MongoDB

/upload_remote_file
仅支持post请求
参数：上传的file文件

功能：解析上次的data文件，并将其内容存入mongoDB

/export_data
仅支持get请求
参数：无

功能：将MongoDB中的数据，导出到本地 ../../data/files 文件夹的 test.json 文件中
