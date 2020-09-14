import datetime
import os
import random
import sqlite3
import time

import requests
import schedule
from uiautomator import device as d


def init():
    # 点亮屏幕
    os.popen("adb shell input keyevent 224")
    time.sleep(1)

    # 滑动屏幕
    os.popen("adb shell input swipe 300 2000 300 500")
    time.sleep(1)

    # 返回桌面
    os.popen("adb shell input keyevent 3")


def start_work():
    time.sleep(3)
    # 打开企业微信
    os.popen("adb shell am start com.tencent.wework/com.tencent.wework.launch.LaunchSplashActivity")
    time.sleep(5)

    d(text=u"工作台").click()
    time.sleep(1)

    os.popen("adb shell input swipe 300 2000 300 500")
    time.sleep(2)

    d(resourceId='com.tencent.wework:id/es3').click()
    time.sleep(3)

    msg = '打卡失败，不在范围内'
    if '在打卡范围内' in d(resourceId="com.tencent.wework:id/ij").info['text']:
        text = d(resourceId="com.tencent.wework:id/ar0").info['text']
        if text == '上班打卡':
            d(resourceId="com.tencent.wework:id/ar0").click()
            time.sleep(2)

            if d(text=u"上班·正常").info['text'] == "上班·正常":
                in_time = d(className="android.widget.TextView", resourceId="com.tencent.wework:id/mp").info['text']
                print("打卡时间：", in_time)
                msg = "上班打卡成功: 时间：" + in_time + " 日志时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                msg = "打卡失败:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            d(resourceId="com.tencent.wework:id/ar0").click()
            time.sleep(2)

            if d(text=u"下班·正常").info['text'] == "下班·正常":
                in_time = d(className="android.widget.TextView", resourceId="com.tencent.wework:id/mp").info['text']
                msg = "下班打卡成功: 时间：" + in_time + " 日志时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                msg = "打卡失败:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 按返回键
    os.popen("adb shell input keyevent 4")
    time.sleep(2)

    # 返回桌面
    os.popen("adb shell input keyevent 3")
    time.sleep(1)

    # 锁屏
    os.popen("adb shell input keyevent 26")

    return msg


def send_message(msg, is_morning):
    token = 'AT_fGdBD04yc7eFditfK1KPevaWW38QdCB9'
    uid = 'UID_LidIVDdyoPmj0zOwpIqDosW5vIS8'
    msg = ("上午打卡\n" if is_morning else "下午打卡\n") + msg
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken={}&uid={}&content={}'.format(token, uid, msg)

    print(requests.get(url).text)


def get_random_minute():
    return int(random.random() * 15)


def get_holiday_or_except(year):
    conn = sqlite3.connect(os.path.split(os.path.realpath(__file__))[0] + '/holiday')
    items = conn.execute('select * from holiday where year = {}'.format(year))

    holiday = []
    need_work = []

    for item in items:
        if item[3] == 0:
            need_work.append(item[1])
        else:
            holiday.append(item[1])

    return holiday, need_work


def main():
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    weekday = now.weekday()
    is_morning = now.hour < 12

    get_holiday_or_except(now.year)
    holiday, need_work = get_holiday_or_except(now.year)

    #
    # # 随机sleep
    # time.sleep(get_random_minute() * 60)

    # 打开屏幕，开始处理
    init()

    if today in holiday:
        send_message(today + '是节假日休息，不需要打卡哦', is_morning)
    elif weekday == 5 or weekday == 6:
        if today in need_work:
            ret = start_work()
            send_message(today + '打卡结果：' + ret, is_morning)
        else:
            send_message(today + '是周末，不需要打卡哦', is_morning)
    else:
        ret = start_work()
        send_message(today + '打卡结果：' + ret, is_morning)


if __name__ == '__main__':
    schedule.every().day.at("08:10").do(main)
    schedule.every().sunday.monday.wednesday.friday.saturday.at("18:10").do(main)
    schedule.every().thursday.tuesday.at("21:10").do(main)

    while True:
        schedule.run_pending()
        time.sleep(3)

