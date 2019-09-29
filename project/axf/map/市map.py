from pyecharts import Map

quxian = ['观山湖区', '云岩区', '南明区', '花溪区', '乌当区', '白云区', '修文县', '息烽县', '开阳县', '清镇市']

values3 = [3, 5, 7, 8, 2, 4, 7, 8, 2, 4]

map3 = Map("贵阳地图", "贵阳", width=1200, height=600)

map3.add("贵阳", quxian, values3, visual_range=[1, 10], maptype='贵阳', is_visualmap=True)

map3.render(path="贵阳地图.html")
