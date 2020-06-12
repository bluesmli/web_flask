import time


def format_time():
    '''
    :return: 格式化当前时间
    '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
