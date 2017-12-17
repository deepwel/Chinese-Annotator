

# Chinese Anotator

> 中文标注工具的前端项目，项目采用前后端分离的结构进行开发。使用Vue.js作为前端的主框架。
> 使用json-server作为mock服务器

## Build Setup

``` bash

# 安装依赖
npm install

如果遇到安装问题可以尝试使用 [cnpm](http://npm.taobao.org/)

# 使用以下命令后，安装[json-server](https://github.com/typicode/json-server)作为mock server
npm install json-server -g

# 启动 mock server
npm run mock

# 使用以下命令进入开发模式，可以访问localhost:8080
npm run dev

# 开发时，可以修改buildconfig/webpack.dev.conf.js中的 SERVER_BASE_URL 来重新指定服务器的地址
'SERVER_BASE_URL': "http://localhost:3000/"

```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
