#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'guige'

from datetime import date
from tqsdk import TqApi, TqAuth, TqBacktest, TargetPosTask

'''
如果当前价格大于10秒K线的MA15则开多仓 (使用 insert_order() 函数)
如果小于则平仓
'''
api = TqApi(backtest=TqBacktest(start_dt=date(2021, 1, 1), end_dt=date(2021, 3, 18)),web_gui="http://192.168.1.4:9876", auth=TqAuth("nuswgg", "541278"))
# 获得 m2105 10秒K线的引用
# klines = api.get_kline_serial("DCE.m2105", 10)
klines = api.get_kline_serial("SHFE.cu2105", 10)


# 判断开仓条件
while True:
    api.wait_update()
    if api.is_changing(klines):
        ma = sum(klines.close.iloc[-15:]) / 15
        print("最新价", klines.close.iloc[-1], "MA", ma)
        if klines.close.iloc[-1] > ma:
            print("最新价大于MA: 市价开仓")
            api.insert_order(symbol="DCE.m2105", direction="BUY", offset="OPEN", volume=5)
            break
# 判断平仓条件
while True:
    api.wait_update()
    if api.is_changing(klines):
        ma = sum(klines.close.iloc[-15:]) / 15
        print("最新价", klines.close.iloc[-1], "MA", ma)
        if klines.close.iloc[-1] < ma:
            print("最新价小于MA: 市价平仓")
            api.insert_order(symbol="DCE.m2105", direction="SELL", offset="CLOSE", volume=5)
            break
# 关闭api,释放相应资源
api.close()