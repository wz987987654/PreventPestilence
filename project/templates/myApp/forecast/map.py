from pyecharts import Geo

keys = ['上海', '北京', '合肥', '哈尔滨', '广州', '成都', '无锡', '杭州', '武汉', '深圳', '西安', '郑州', '重庆', '长沙', '贵阳', '乌鲁木齐']
values = [4.07, 1.85, 4.38, 2.21, 3.53, 4.37, 1.38, 4.29, 4.1, 1.31, 3.92, 4.47, 2.40, 3.60, 1.2, 3.7]

geo = Geo("全国主要城市空气质量热力图", "data from pm2.5", title_color="#fff", title_pos="left", width=1200, height=600,
          background_color='#404a59')

geo.add("空气质量热力图", keys, values, visual_range=[0, 5], type='effectScatter', visual_text_color="#fff", symbol_size=15,
        is_visualmap=True, is_roam=True)  # type有scatter, effectScatter, heatmap三种模式可选，可根据自己的需求选择对应的图表模式
geo.render(path="全国主要城市空气质量热力图.html")