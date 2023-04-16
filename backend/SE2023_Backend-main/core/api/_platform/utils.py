import datetime

def format_time(time):
    # 格式化时间，2019-09-09 12:23:33
    # 去掉毫秒
    if time != None:
        time = str(time)[0:19]
    else:
        print(2)
    return time


def get_field(field):
    # 获得需求领域
    NEED_FIELD_CHOICES = {
        0: '信息技术',
        1: '装备制造',
        2: '新材料',
        3: '新能源',
        4: '节能环保',
        5: '生物医药',
        6: '科学创意',
        7: '检验检测',
        8: '其他'
    }
    return NEED_FIELD_CHOICES[field]


def get_need_state(state):
    # 获得需求状态
    NEED_STATE = {
        0: '进行中',
        1: '已结束',
        2: '未发布'
    }
    return NEED_STATE[state]


def get_order_state(state):
    # 获得订单状态
    ORDER_STATE = {
        0: "待接受",
        1: "正在合作中",
        2: "已拒绝",
        3: "合作结束"
    }
    return ORDER_STATE[state]

def get_now_time(): 
    # 获取标准格式的当前时间
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")