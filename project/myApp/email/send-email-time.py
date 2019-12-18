class EmailManager:
    def __init__(self, **kwargs):
        ...

    def __get_cfg(self, key, throw=True):
        ...

    def __init_cfg(self):
        ...

    def login_server(self):
        ...

    def get_main_msg(self):
        ...

    def get_attach_file(self):
        ...

    def _format_addr(self, s):
        ...

    def send(self):
        ...


# 第二种方式，使用python任务定时运行库 schedule 模块
def send_mail_by_schedule(manager):
    schedule.every(5).minutes.do(manager.send())  # 每5分钟执行一次
    schedule.every().hour.do(manager.send())  # 每小时执行一次
    schedule.every().day.at("23:00").do(manager.send())  # 每天23:00执行一次
    schedule.every().monday.do(manager.send())  # 每周星期一执行一次
    schedule.every().wednesday.at("22:15").do(manager.send())  # 每周星期三22:15执行一次

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    manager = EmailManager(**mail_cfgs)
    send_mail_by_schedule(manager)














