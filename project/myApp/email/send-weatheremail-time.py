# -*- coding: utf-8 -*-
import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from urllib import request
from bs4 import BeautifulSoup
from xpinyin import Pinyin
pin = Pinyin()
# 选择省市
def choice():
    print('请输入1代表直辖市,2代表非直辖市')
    num = input()
    if num == '1':
        city = input("请输入城市:")
        city_pin = pin.get_pinyin(city, '')
        get_info(None, city_pin, None, city)
    else:
        prov = input("请输入省份:")
        city = input("请输入城市:")
        if prov == '陕西':
            prov_pin = 'shaanxi'
            city_pin = pin.get_pinyin(city, '')
            get_info(prov_pin, city_pin, prov, city)
        else:
            prov_pin = pin.get_pinyin(prov, '')  # 将次半1为斑查
            city_pin = pin.get_pinyin(city, '')
            get_info(prov_pin, city_pin, prov, city)
# 获取省市天气信息
def get_info(prov_pin, city_pin, prov, city):
    if prov_pin == None:
        url = 'https://tianqi.moji.com/weather/china/'
        url = url + city_pin + '/' + city_pin
    else:
        url = 'https://tianqi.moji.com/weather/china/'
        url = url + prov_pin + '/' + city_pin
        print(url)

    # 获取天气信息begin#
    htmlData = request.urlopen(url).read().decode('utf8')
    data = BeautifulSoup(htmlData, 'lxml')
    #data = BeautifulSoup(htmlData)
    # print(data.prettify())
    weather = data.find('div', attrs={'class': "wea_weather clearfix"})
    # print(weather)
    temp1 = weather.find('em').get_text()
    temp2 = weather.find('b').get_text()
    # 使用select标签时 如果class中有空格 将空格改为"."才能筛选出来
    # 正则表达式爬取
    AQI = data.select(".wea_alert.clearfix > ul > li > a > em")[0].get_text()
    H = data.select(".wea_about.clearfix > span")[0].get_text()  # 湿度
    S = data.select(".wea_about.clearfix > em")[0].get_text()  # 风速
    if city_pin == 'beijing' or city_pin == 'tianjin':
        B = data.select(".wea_about.clearfix > b")[0].get_text()  # 限行  只有北京和天津才有
    A = data.select(".wea_tips.clearfix > em")[0].get_text()  # 今日天气提示
    C = list(data.select(".live_index_grid > ul > li")[1].get_text().strip())# 紫外线
    C = C[0] + C[1]

    date = str(datetime.date.today())  # 获取当天日期
    if city == '北京' or city == '天津':
        weather_info = '来自疾病预警系统的贴心提示\n' + city + '市' + ',' + date + '\n' + '实时温度: ' + temp1 + '℃' + ',' + temp2 + '\n'  '湿度：' + H + '\n' '风速：' + S + '\n' '紫外线：' + C + '\n' '今日提示：' + A + '\n' + '今日限行：' + B
    elif city == '上海' or city == '重庆':
        weather_info = '来自疾病预警系统的贴心提示\n' + city + '市' + ',' + date + '\n' + '实时温度: ' + temp1 + '℃' + ',' + temp2 + '\n'  '湿度：' + H + '\n' '风速：' + S + '\n' '紫外线：' + C + '\n' '今日提示：' + A
    else:
        weather_info = '来自疾病预警系统的贴心提示\n' + prov + '省' + city + '市' + ',' + date + '\n' + '实时温度: ' + temp1 + '℃' + ',' + temp2 + '\n'  '湿度：' + H + '\n' '风速：' + S + '\n' '紫外线：' + C + '\n' '今日提示：' + A

    # 获取明日天气
    tom = data.select(".days.clearfix ")[1].find_all('li')
    # print(tom)
    temp_t = tom[2].get_text().replace('°', '℃') + ',' + tom[1].find('img').attrs['alt']  # 明天温度
    S_t1 = tom[3].find('em').get_text()
    S_t2 = tom[3].find('b').get_text()
    S_t = S_t1 + S_t2  # 明日风速
    A_t = tom[-1].get_text().strip()  # 明日空气质量
    info_t = '\n明日天气：\n' + '温度：' + temp_t + '\n' + '风速：' + S_t + '\n' '空气质量：' + A_t + '\n'
    # 定义一个tips的字典

    tips_dict = {'cold': '感冒预测', 'makeup': '化妆指数', 'uray': '紫外线量', 'dress': '穿衣指数', 'car': '关于洗车', 'sport': '运动事宜'}
    info_tips = ''
    # print(list(tips_dict.keys()))

    for i in list(tips_dict.keys()):
        url_tips = url.replace('weather', i)
        htmlData = request.urlopen(url_tips).read().decode('utf8')
        data = BeautifulSoup(htmlData, 'lxml')
        tips = data.select(".aqi_info_tips > dd")[0].get_text()
        info_tips = info_tips + tips_dict.get(i) + ':' + tips + '\n'
    global info_all
    info_all = weather_info + '\n' + info_tips + info_t

# 发送邮件
def send_email():
    sender = "18360939363@163.com"  # 发件人
    password = "211416038A"  # 授权码
    receiver = str(input('请输入收件人邮箱地址：'))  # 收件人
    try:
        mail = MIMEText(info_all, 'plain', 'utf-8')  # 邮件内容
        mail['Subject'] = Header('预警系统通知', 'utf-8')  # 邮件主题
        mail['From'] = sender  # 发件人
        mail['To'] = receiver  # 收件人
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', 25)  # 连接邮箱服务器
        smtp.login(sender, password)  # 登录邮箱
        smtp.sendmail(sender, receiver, mail.as_string())  # 第三个是把邮件内容变成字符串
        smtp.quit()  # 发送完毕，退出
        print('\n邮件已成功发送！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    choice()

    send_email()
