Text Classification

# 加载过程

## Situation 1: 冷启动
所有数据均未打上标签(label)
导入数据
可以将数据 按照需要标注的格式 一次性导入到dataset表中


## Situation 2: 第二次
已经有训练过的model


# Online 标注过程
### step 1: 用户点击页面上的评价按钮 例如：accept 
### step 2: 通过ajax方式 异步调用后台的 accept api
前端传过来的请求参数(request param) 
```javascript
{
	"_id":ObjectId("dfjl32jljfdlsjldf"),
	"label":"org",
	"action","accept"
}
```


accept: 根据_id 更新 dataset表数据

同时将操作保存到history表中

### step 2.5 api内部的执行过程
调用/models/online当中的方法:
```python
def do_online_annotation(text, ):
	"""
	@param text 待标注文本
	"""
	return {"label":"org"}
```





### tep 3: 存放到mongodb 数据库中

表： dataset
目标数据集
```javascript
{
	"_id": ObjectId("dfjl32jljfdlsjldf")
	"text":"联想"，
	"label":"org",
	"confidence":.9，
	"labeled":true/false # 是否标注过,
	"source":"newyork news"
}
```


表： history
单条标注的操作记录
```javascript
{
	"_id": ObjectId("dfjl32jljfdlsjldf")  # 关联到to_be_labeled
	"action":"accept" # enum type: accept reject ignore cancel
	"datatime":"2017-11-13 15:13:24" # 操作的时间
}
```

### step 4: 后台api 返回json格式的结果 到前端用户
```javascript
{
	"code": 200, # 状态码  200：成功
	"msg": "标注成功", # 提示信息
	"data":{} # 后端返回的dataset
}
```


### step 5: 前端页面根据 api返回结果 更新页面
例如： 后端api返回 标注成功

### step 6: 从未标注的数据集当中 加载一条新的待标注数据
前端页面再次加载dataset表中 未标注的数据到前端

### step 7: 循环step 1-6

# Offline标注过程
Mongodb系统自动触发 无需用户干预
### step 1: 当labeled表中数据量达到一个阀值的时候，触发离线计算 更新model 触发机制待定
### step 2:
调用/models/offline当中的方法:
```python
def do_offline_annotation(collection, ):
	"""
	@param collection 待标注的表名称
	"""
	return {"label":"org"}
```

### step 3: 将更新的model 用于未标注过的数据 添加一遍confidence

# 系统配置 config
在/config包中 添加配置文件 暂定使用python文件作为配置文件

例如：
config.py
```python
TRIGGER_OFFLINE_BATCH_SIZE = 1000 # 触发offline计算的阀值
```

