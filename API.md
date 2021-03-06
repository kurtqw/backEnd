## 1. 聊天部分

### 1.1 返回用户ID
**url**
```
119.29.161.184:8000?rand=xxx&sex=xxx&nameIndex=xxx
```
*sex : 0为male 1为female*  
**response**  
success:
```
{
  "status":1,
  "id":"xsijfa-r21ja2j-asoj2aa-adh2saj",
}
```

### 1.2 聊天
**url**
```
119.29.161.184:8000/chat
```
**params**
```
id : string(用接口1.1返回的ID)
```
**request**
```
{
  "type":"xxxx",
  "text":"xxxxxxx",
  "id":"xxxxxx-xxxx-xxxxx"
}
```

**response**
```
{
  "res":{
    "sender":"xxx",
    "type":"xxx",
    "content":"",
    "time":"2016-10-16  13:45:20"
  },
  "status":1
}

```


*该接口使用websocket协议*


### 1.3 返回昵称
**url**
```
119.29.161.184:8000/name?sex=xxx
```
**response**
```
{
  res: {
      7: "郭芙",
      11: "李莫愁",
      16: "李沅芷",
      24: "方怡",
      28: "何红药",
      31: "安小惠",
      37: "杨不悔",
      41: "袁紫衣"
      },
  status: 1
}
```
*sex : 0为male 1为female*


### 1.4 返回对方昵称
**url**
```
119.29.161.184:8000/othername?id=xxx
```
**response**
```
{
  res:{'mine': "郭芙",'other':"对面那个"}
  status: 1
}
```


### 1.5 群聊
**url**
```
119.29.161.184:8000/groupchat?topic=泡馆&rand=xxxx
```
**params**
```
rand : 随机数
```
**request**
```
{
  "type":"xxxx",
  "text":"xxxxxxx",
  "id":"xxxxxx-xxxx-xxxxx"
}
```

**response**
```
websocket建立连接后：
{
  "id":"xxxxxx-xxxx-xxxxx",
  "status" : 1,
  "name" : "就是个名字",

}

聊天进行时：
{
  "res":{
    "sender":"xxx",
    "type":"xxx",
    "content":"",
    "time":"2016-10-16  13:45:20"
  },
  "status":1
}

```


*该接口使用websocket协议*

### 2. 热点新闻和笑话部分
### 1.1 返回热点新闻
**url**
```
119.29.161.184:8000/news?page=xxx
(page表示第几页，从 1 开始计数，每页返回十条热点新闻,按照 pv 进行降序排列)
```

**response**
success:
```
{
   "status": 1,
   "data": [{"id":xxx,"url":xxx,"title":xxx,"visit_cnt":xxx},...]

```

fail:
```
{"status": 0, "data": "page exceed limits"}
```

### 1.2 热点新闻访问量更新
**url**
```
119.29.161.184:8000/news (post)

数据格式：
{
	"news_id":"以整数表示",
	"cnt":"以整数表示"
}
如
{
	"news_id":"2",
	"cnt":"1"
}
```

**response**
success:
```
{
   "status":1
}
```

fail:
```
{
  "status":0,
   "data":"XXX" (给出失败原因)
}
```
   

### 1.3 返回笑话
**url**
```
119.29.161.184:8000/joke
(随机返回一个笑话)
```

**response**
success:
```
{
   "status":1,
   "data":"笑话内容"
}
```
fail:
```
{
   "status":0,
   "data":"XXX"
}
```

### 1.4 返回群聊话题
**url**
```
119.29.161.184:8000/topic?type=[sport movie music library game travel]
(随机返回十条数据，其中 sport movie game 数据是新闻 | travel 数据来自蝉游记 | music library 数据来自豆瓣250排行榜)
```

**response**
success:
```
{
   "status":1,
   "data":[
   {'url':'...',
   'title':'...'},
   {'url':'...',
   'title':'...'},
   ...
   ](长度为10)
}
```
fail:
```
{
   "status":0,
   "data":"XXX"
}
```

