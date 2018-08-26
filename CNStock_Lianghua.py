# --coding:utf-8--
#Python3--8/26/2018
#Copyright by EthanLiu
import baostock as bs
import pandas as pd
import numpy as np
import talib as ta
import datetime

def return_constraintdict(stockcodelist):
      login_result = bs.login(user_id='anonymous', password='123456')
      print('login respond error_msg:' + login_result.error_msg)

      startdate = '2018-08-21'  # 开始日期，从2018年1月1日开始
      today = datetime.datetime.now()   # 获取今天的时间 年 月 日 小时 分钟 秒 毫秒 
      delta = datetime.timedelta(days=1)  # 两个时间的差值为1天
      # 获取截至上一个交易日的历史行情
      predate = today - delta  # 今天的时间 减去 两时间差值，定义为 predate 上一日这个时候的时间值
      strpredate = datetime.datetime.strftime(predate, '%Y-%m-%d')  # strpredate 是用 strftime 格式化后的 上一日时间表示
      print (strpredate) # 打印上一天的日期，格式化过的：年-月-日
      for stockcode in stockcodelist:
          rs = bs.query_history_k_data("%s" % stockcode, "date,code,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM", start_date=startdate, end_date=strpredate, frequency = "d", adjustflag="2")
          # rs 为从bs中查询到的 该股票的(按从2018年1月1日起每一日的)k线数据信息，一共有14列 
          print('query_history_k_data respond error_code:' + rs.error_code)
          print('query_history_k_data respond error_msg:' + rs.error_msg)
          # print (rs)  <baostock.data.resultset.ResultData object at 0x00000000144FDC50>  (是一个数据集)

      # 打印结果集
          result_list=[]  # 结果列表 下面用 append 逐步添加数据
      while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            result_list.append(rs.get_row_data())   # 将 rs row_data/行数据 添加到result_list 中去
            print (result_list) # 打印 result_list 结果集里的数据
            result = pd.DataFrame(result_list,columns=rs.fields)  # 定义一个 result 变量， 用pd.DataFrame的2个参数 result_list和 columns=rs.fields处理
            print (result)  # result 是一个类，被 pandas.core.frame.DataFrame 定义
            #print (type(result))
            closelist = list(result['close'])
            closelist = [float(price) for price in closelist]

            # 调用 TA-Lib 中的 MA 函数， 计算20日均线值
            malist = ta.MA(np.array(closelist),timeperiod = 20)
            if len(malist) > 20 and closelist[-20] > 0:
                    ma20value = malist[-1]
                    summit20day = max(closelist[-10:])
                  # 以突破10日高点且在20日均线以上作为买入条件
                    resistancelinedict[stockcode] = max(ma20value,summit20day)
            else:
                    resistancelinedict[stockcode] = float(closelist[-1])
                    bs.logout()
      return resistancelinedict


# 每次收到实时行情后，回调此方法
def callbackFunc(ResultData):
# print (ResultData.data)
      for key in ResultData.data:
      # 当盘中价格高于警示价格， 输出提示信息。
          if key in resistancelinedict and float(ResultData.data[key][6]) > resistancelinedict[key]:
               print ("%s, 突破阻力线，可以买入" %key)

def test_real_time_stock_price(stockcode):
      login_result = bs.login_real_time(user_id='anonymous', password='123456')
      # 订阅
      rs = bs.subscribe_by_code(stockcode, 0, callbackFunc, "", "user_params")
      # rs = bs.subscribe_by_code("sz.300009", 0, callbackFunc, "", "user_params")
      if rs.error_code != '0':
            print("request real time error", rs.error_msg)
      else:
      #使主程序不再向下执行。 使用 time.sleep()等方法也可以
            text = input("press any key to cancel real time \r\n")
      # 取消订阅
            cancel_rs = bs.cancel_subscribe(rs.serial_id)
      # logout
            login_result = bs.logout_real_time("anonymous")
      

if __name__ == '__main__':
      resistancelinedict = {}
      # 自定义股票池
      stockcodelist = ['sh.600000']
      stockcodes = ""
      for stockcode in stockcodelist:
          stockcodes = "%s%s," %(stockcodes, stockcode)
          stockcodes = stockcodes[:-1]
          print (stockcodes)
      resistancelinedict = return_constraintdict(stockcodelist)
      #### logout system ####
test_real_time_stock_price(stockcodes)
                      

return_constraintdict(stockcodelist)
