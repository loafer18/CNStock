# --coding:utf-8--
#Python3--8/26/2018
#Copyright by EthanLiu
import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import time, datetime
import csv

global li,stkPriLi,stkNameList
sum_li = []
stkPriLi = []
stkNameList = []


stock_price_url = 'http://hq.sinajs.cn/list=sz300260,sz000963,sz300357'

# 需要定义一个 获取单个股票价格列表的函数
# 根据URL 地址，创建 3 个列表，每一个列表名字都用股票代码
# 然后依次 append 新的数据到列表中
#def singelStkPri():
#    graph_data.stkID

def sleeptime(hour,min,sec):                      
    return hour*3600 + min*60 + sec;
    # 可计算 如果有小时和分钟 后，总的休眠秒数
second = sleeptime(0,0,1)
# 隔1秒
# 先获取系统当前时间，显示出来，
print (time.strftime('Current Time： %Y-%m-%d, %I:%M:%S',time.localtime()))
# print ('Next Run Time: '+ time.strftime('%I:(%M+1):00',time.localtime()))
Year= (time.strftime('%Y', time.localtime()))
Month= (time.strftime('%m', time.localtime()))
Day= (time.strftime('%d', time.localtime()))
Hour= (time.strftime('%H', time.localtime()))
# 注意,这里 %I 是12小时制时间，和下面 datetime.datetime.now()比，如果下午的时间相比，将会变小
# 使用 %H 24小时制的时间，才能正确的比较
Minu= (time.strftime('%M', time.localtime()))

#print (Year, Month, Day, Hour, Minu)
#print (type(Minu)) # 表明 取出的各种时间数值是 str 属性，而非数值属性
if int(Minu)== 59:  # 时间为59分钟时
    nextMinu= 0    # 下一分钟为0，
    Hour = int(Hour)+1  # 小时增加1
else:
    nextMinu = int(Minu)+1 #当前时间的下一分钟

print ('Next Minute will be: ',nextMinu)  #此时分钟属性为数值(int整型)
nextExeTime= datetime.datetime(int(Year), int(Month), int(Day), int(Hour), nextMinu, 0)
print ('Program will start at: ', nextExeTime)
#print (nextExeTime)
# 取出上述时间的分钟数， 然后加1， 设定为程序执行的新的时间  
# 再进行计算，需要等待多少秒，到一个整数小时/分钟
# 执行时间是 现在时间加N秒,到下一个分钟，整数秒进行执行。
# sleep = sleeptime(0,0,60-%S)
# 到整数小时/分钟 时候，开始下面的


def bytespdate2num (fmt, enconding = 'utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

# stock 名称列表是不需要增量的，所以需要单独列出来获取名称列表即可

def stock_name(stock):   
    # 定义一个函数，获取多个 stock 数据，并整理数据，返回股票名称及建立 csv 文件
    # CSV 文件初始化函数
#    stock_price_url = 'http://hq.sinajs.cn/list=sz300260,sz000963,sz300357'
    source_code = urllib.request.urlopen(stock_price_url).read()
#    print (source_code)
    sort_data = str(source_code)
#    print (sort_data) # 后期不需要打印
    li = sort_data.split(';')  # 一个临时列表，将上面获取的数据用 分号; 分隔出来
#    print (li[0])     # 打印第一个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[1])     # 打印第二个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[2])     # 打印第三个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[3])     # 打印第四个元素
    
#    sum_li = []
#    stkPriLi = []
#    stkNameList = []
    for i in range (len(li)-1):
#   循环遍历开始 循环数量为 所有获取的数据（stock个数数据分隔后的数量）分隔后数量
        stkID = li[i][13:21]  # 取出第 i 个 stock 代码
#        print (stkID)
        stockName = str(stkID)   
#        print (stockName)  # 打印出当前的 stock 名称
#        stkPriLi.append(stkPri)
        stkNameList.append(stockName)
#        print (stkPriLi)  # 打印出当前的 stock price list
        output = open(stkID+'.csv','w')    # 在首次执行的时候生成 CSV 文件
#        print (stkID+'.csv')  # # 打印出当前的 stock 的 csv 文件名
        # 下面将每一个 stock 的每一次值都 append 到这个新的 csv 文件中
        with open(stkID+'.csv','a+') as csvfile:
#            spamwriter = csv.writer(csvfile, delimiter=',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
#            spamwriter.writerow(stkPriLi)
             csvfile.close()

# stock 价格， 是需要按时间增量的，所以可以用下面的函数，通过最后面的反复循环不断读取数据


#stock_name('TSLA')
# 调用 stock_name 函数，取出股票名称，及建立对应的 csv 文件。
# 如果注销该命令，则不进行CSV文件初始化动作，则不会清空现有文件。

def graph_data(stock):   
    # 定义一个函数，获取多个 stock 数据，并整理数据，返回值为所有股票 某一时间点的价格，并写入上面创建的 csv 文件    
#   stock_price_url = 'http://hq.sinajs.cn/list=sz300260,sz000963,sz300357'
    source_code = urllib.request.urlopen(stock_price_url).read()
#    print (source_code)

    sort_data = str(source_code)
#    print (sort_data) # 后期不需要打印
    li = sort_data.split(';')
#    print (li[0])     # 打印第一个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[1])     # 打印第二个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[2])     # 打印第三个元素
#    print ('\n')      # 打印一个分隔行
#    print (li[3])     # 打印第四个元素
    
#    sum_li = []
#    stkPriLi = []
#    stkNameList = []
    for i in range (len(li)-1):
#   循环遍历开始 循环数量为 所有获取的数据（stock个数数据分隔后的数量）分隔后数量
        stkID = li[i][13:21]  # 取出第 i 个 stock 代码
#        print (stkID)
#        stockName = str(stkID)
#        stockLi = stockName
#        print (stockLi)  # 打印出当前的 stock 名称  由于上一个函数 stock_name已经获取了股票名称，
#                         # 所以这里获取股票名称的代码不需要重复

        stkPri = li[i][70:76]  # 取出第 i 个 stock 现价
#        print (stkPri)   # 打印出第 i 个 stock 现价
        stk = [stkID, stkPri]  # 组合成一个 stock 代码和现价数值列表

        sum_li.append(stk)    # 将每个股票的信息（名称，价格）都加入汇总表
        stkPriLi.append(stkPri)  # 合并 股票价格，到一个价格列表中
#        stkNameList.append(stockName)
#        print (stkPriLi)  # 打印出当前的 stock price list
#        output = open(stkID+'.csv','w')    # 在首次执行的时候生成 CSV 文件
#        print (stkID+'.csv')  # # 打印出当前的 stock 的 csv 文件名
        # 下面将每一个 stock 的每一次值都 append 到这个新的 csv 文件中
        with open(stkID+'.csv','a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',quotechar = '|', quoting = csv.QUOTE_MINIMAL)
            spamwriter.writerow([stkPri])
#        stockNameList = []  在这里获取股票列表 行不通
#        stockNameList = stockNameList.append(stockLi)
#        print (stockNameList)

#        print (output)   # 打印出各 CSV output
#        print (stkPri)    # 得到 股票（此时此刻）价格列表
#        print (stkNameList) # 得到 股票名称列表 
    print (sum_li[-3:], time.strftime('%m/%d %I:%M:%S',time.localtime(time.time())))
    # 打印 股票名称+股票此时此刻价格组合列表的最后3个数据，即最新数据，再加当前时间

    # print (sum_li ,time.strftime('%m/%d %I:%M',time.localtime(time.time())))
    # 打印新的列表， 后面跟一个日期 时间，  格式： 月/日 小时：分钟: 秒 （12小时制）

# CSV Files Creation

#   写模式打开一个 CSV 文件，然后将上面 graph_data 函数数据写入该 CSV 文件
  
    # 这里需要将要写入的数据进行格式化处理
    # 新建一行， 行号 取名为 new_li[0][0]
    # 新建第二行，行第一个数值为 new_li[0][1], 以 i 进行循环
#    for i in range (len(li)-1):

#    stkCSV.close()
        
#    print (stkCSV)

#   周五早上做梦, 梦到自己赚了好多钱, 好像是支票,都印在A4纸上，每张纸上都印着 几点几几美金，
#   我有一大包这样的支票，放在书包里，拿到银行， 银行服务人员还每张纸给我计算，还按当天汇率给折算成人民币给存入
#   真的开心， 发达了；  
    
#    print (new_li)  


#    stock_data = []
#    split_source = source_code.split('\n')
#    for line in split_source:
#        split_line = line.split(',')
#        if len(split_line) == 6:
#            if 'values' not in line and 'labels' not in line:
#        stock_data.append(line)

#    date, closep, highp, lowp, openp, volumn = np.loadtxt(stock_data,
#                                                          delimiter = ',',
#                                                          unpack = True,
                                                          # %Y = full year. 2018
                                                          # %y = partial year.18
                                                          # %m = number month
                                                          # %d = number day
                                                          # %H = hours
                                                          # %M = minutes
                                                          # %S = seconds
                                                          # 12-06-2018
                                                          # %m-%d-%Y
#                                                          converters = {0: bytespdate2num('%Y%m%d')})
#    plt.plot_date(date, closep,'-', label = 'Price')

#    plt.xlabel('Date/Time')
#    plt.ylabel('Price')
#    plt.title(stkID)
#    plt.legend()
#    plt.show()    暂时停止显示图片


#while datetime.datetime.now() < nextExeTime:
#    time.sleep(1)

#while 1==1:   # 后续需要将时间限制为 从 9:25AM 开始， 15:00PM

#print (datetime.datetime.now())
#print (nextExeTime)
#print (datetime.datetime.now() < nextExeTime)



while 1==1:
    if datetime.datetime.now() < nextExeTime:
        print ("Sleep 1 sec")
        time.sleep(second)
    else:         
        graph_data('TSLA')
        time.sleep(1)
        
        #datetime.datetime.now() == nextExeTime:
        #print ('Start program')  
#    print ('do action',time.strftime('%m/%d %I:%M',time.localtime(time.time())))
    # 用特定的日期时间格式，在 do action 的同时，在后面打印出需要的时间：月/日 小时：分钟
#        print (stkID, li[2],time.strftime('%m/%d %I:%M',time.localtime(time.time())))
    
            # 调用函数 -> 获取数据，


#  在每一个整数时间点，将数值写入一个列表，并组成新的 价格列表

# how to get 准点分钟均值？
# 未来添加功能：获取当前星期，时间， 并判断，如果非交易时间段，打印出 非交易时间 提醒或者打印出最后一个交易日的收盘价
