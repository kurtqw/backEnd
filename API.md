## 1. 聊天部分
### 1.1 返回用户ID
**url**
```
119.29.161.184:8000?rand=xxx&sex=xxx
*sex 0:male 1:female*
```
**response**  
success:
```
{
  "status":1,
  "id":"xsijfa-r21ja2j-asoj2aa-adh2saj"
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
*该接口使用websocket协议*
