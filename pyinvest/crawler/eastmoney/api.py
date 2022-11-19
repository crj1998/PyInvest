import random
import requests

import pandas as pd

from pyinvest.crawler.eastmoney.const import F_MAPPING, UT, HEADERS, TIMEOUT


def fund_list_page(
    fs='b:MK0021,b:MK0022,b:MK0023,b:MK0024', 
    fid='f3', 
    fields='f2,f3,f4,f5,f6,f7,f8,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22,f11,f62'
):
    params = {
        'pn': 1,
        'pz': 20, # 每页大小
        'po': 1, # 排序方向（正序填0，倒序填1，默认为1。）
        'fid': fid,  # 排序字段
        'np': 1,
        'fs': fs,  # 证券过滤器
        'fields': fields,       # 需要获取的字段
        'ut': UT,
        'fltt': 2,
        'invt': 2,
    }
    headers = {}
    headers.update(HEADERS)
    url = f'http://{random.randint(1, 99)}.push2.eastmoney.com/api/qt/clist/get'
    r = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
    assert r.ok

    df = pd.DataFrame(r.json()['data']['diff'])
    df['f6'] = df['f6'] / 10e4
    df = df.rename(
        columns = {
            'f2': '最新价',
            'f3': '涨跌幅', 
            'f4': '涨跌额', 
            'f5': '成交量', 
            'f6': '成交额',
            'f7': '振幅',
            'f8': '换手率',
            'f10': '量比',
            'f11': '5分钟涨跌',
            'f12': '代码', 
            'f13': '市场',
            'f14': '名称', 
            'f15': '最高价',
            'f16': '最低价',
            'f17': '开盘价',
            'f18': '昨收',
            'f20': '总市值',
            'f21': '流通市值',
            'f22': '涨速',
            'f24': '60日涨跌幅',
            'f25': '年初至今涨跌幅',
            'f62': '主力净流入'
        }, inplace = False
    )

    return df


# 获取K线图数据
def get_kline(code, **kwargs):
    params = {
      'secid': code,
      'ut': UT,
      'fields1': 'f1,f2,f3,f4,f5,f6',
      'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
      'klt': 101,  # k线类型：日K D = 101, 周K W = 102, 月K M = 103, 5分钟K M5 = 5, 15分钟K M15 = 15, 30分钟K M30 = 30, 60分钟K M60 = 60
      'fqt': 0,    # 除复权类型：不复权Bfq 0, 前复权Qfq 1, 后复权Hfq 2
      'beg': 0,    # 开始日期
      'end': 20500101, # 结束日期
      'smplmt': 1000, # 均匀返回最多多少条
      'lmt': 1000 # 最近多少条数据
    }

    params.update(kwargs)

    if 'lastcount' in kwargs:
        params['lmt'] = kwargs['lastcount']
        del params['lastcount']
        del params['beg']
        del params['smplmt']

    url = f'http://{random.randint(1, 99)}.push2his.eastmoney.com/api/qt/stock/kline/get'
    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    assert r.ok
    data = r.json()
    df = pd.DataFrame(
        [i.split(',') for i in data['data']['klines']], 
        columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'],
    )
    df = df.set_index('日期', drop=True)
    df[df.columns] = df[df.columns].apply(pd.to_numeric)

    df['成交量'] = (df['成交量'] / 10e6).round(1)
    df['成交额'] = (df['成交额'] / 10e9).round(1)

    return df

    # fig, ax=plt.subplots(1, 1, figsize=(15,6))
    # https://blog.csdn.net/Shepherdppz/article/details/117575286
    # df4plot = df[['开盘', '最高', '最低', '收盘', '成交量']]
    # df4plot = df4plot.rename(
    #     columns={'开盘': 'Open', '最高': 'High', '最低': 'Low', '收盘':'Close', '成交量': 'Volume'}, inplace=False
    # )
    # df4plot.index = pd.to_datetime(df4plot.index)
    # df4plot.index.name = 'Date'
    # my_color = mpf.make_marketcolors(up='r', down='g', edge='inherit', wick='inherit', volume='inherit')
    # # 设置图表的背景色
    # my_style = mpf.make_mpf_style(marketcolors=my_color, figcolor='(0.82, 0.83, 0.85)', gridcolor='(0.82, 0.83, 0.85)')

    # mpf.plot(df4plot, style=my_style, mav=(5, 15, 30), type='candle', volume=True)

    # plt.show()