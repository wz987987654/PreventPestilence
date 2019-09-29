from pyecharts import Map

map2 = Map("贵州地图", '贵州', width=1200, height=600)

city = ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州']

values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]

map2.add('贵州', city, values2, visual_range=[1, 10], maptype='贵州', is_visualmap=True, visual_text_color='#000')

map2.render(path="贵州地图.html")
