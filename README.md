## 企业微信打卡
> 借助旧手机

### `adb` 安装
[文档地址](https://developer.android.com/studio/command-line/adb?hl=zh-cn)
### 相关修改项
#### 新的一年需要打开 `holiday` 添加节假日信息
使用 `sqlite` 数据库管理工具打开并进行添加
#### 注意修改消息推送和执行时间
##### 推送相关
```python
def send_message(msg, is_morning):
    token = 'AT_fGdBD04yc7eFditfK1KPevaWW38QdCB9'
    uid = 'UID_LidIVDdyoPmj0zOwpIqDosW5vIS8'
    msg = ("上午打卡\n" if is_morning else "下午打卡\n") + msg
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken={}&uid={}&content={}'.format(token, uid, msg)
```
可以参考文档进行修改对应信息 [文档](http://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8)
##### 执行时间
```python
schedule.every().day.at("08:10").do(main)
schedule.every().sunday.monday.wednesday.friday.saturday.at("18:10").do(main)
schedule.every().thursday.tuesday.at("21:10").do(main)
```
我们由于周二和周四要固定加班，因此直接在周二和周四单独处理了，如果不需要则可以参考 `08:10` 的添加一个下班时间的打卡即可