# -*- coding:utf-8 -*-
# author: Jaylen Lee time:2023/12/13
import json
import random
import datetime
import time
from hashlib import md5
import collections


# md5(b'123').hexdigest()
# print(bs)

list2 = [0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4a,0x4b,0x4c,0x4d,0x4e,0x4f,0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5a,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x6b,0x6c,0x6d,0x6e,
         0x6f,0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77,0x78,0x79,0x7a,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39]
list3 = ['wechat','alipay','cash']

list4 = ['completed','refunded','unpaid']
list_user_count = []
list_pas_id=[]
list_gap = [1,2,3]#order生成的间隔时间
list_begin = [1,2,3,4,5,6,7,8]# 第一个order生成的时间

std_time = datetime.datetime(2023, 12, 16, 21, 50, 0)
# end_time = std_time + datetime.timedelta(weeks=-4)  # 4*12*4
start_time = std_time + datetime.timedelta(weeks=-192)
start_time_2 = std_time + datetime.timedelta(weeks=-26)#最晚的订单生成于165.5周；这个时间作为当前下订单的参照时间


with open("user.json",'r',encoding='utf-8') as f:
    a = json.load(f)['User']
with open("passenger.json",'r',encoding='utf-8') as f:
    b = json.load(f)['Passenger']
with open("Order.json") as f:
    c = json.load(f)
with open("Person_info.json") as f:
    d = json.load(f)
c_dict = collections.defaultdict(list)
d_dict = collections.defaultdict(list)
# e_dict = collections.defaultdict(list)
for i in c:
    c_dict[i['user_account']].append(i)
for i in d:
    d_dict[i['account']].append(i['id_number'])

for i in range(len(a)):
    list_user_count.append(a[i]['account'])
for i in range(len(b)):
    list_pas_id.append(b[i]['id_number'])

with open("Train.json") as f:
    e = json.load(f)
g_dict = collections.defaultdict(list)
with open("Arrival_time.json") as f:
    g = json.load(f)
for i in g:
    g_dict[i['train_number']].append(i)

# for i in e:
#     e_dict[].append(i[''])

# def create_datetime(n): # order数量
#     # end_time = datetime.datetime.now() + datetime.timedelta(weeks=-4)# 4*12*4
#     # start_time = datetime.datetime.now() + datetime.timedelta(weeks=-192)# 已完成/已退款的时间范围
#     # end_time = datetime.datetime.now() + datetime.timedelta()# 4*12*4
#     # start_time = datetime.datetime.now() + datetime.timedelta(weeks=-4)# 未付款的时间范围
#
#     a1 = tuple(start_time.timetuple()[0:9])  # 设置开始日期时间元组
#     a2 = tuple(end_time.timetuple()[0:9])  # 设置结束日期时间元组
#
#     start = time.mktime(a1)  # 生成开始时间戳
#     end = time.mktime(a2)  # 生成结束时间戳
#
#     # 随机生成日期字符串
#     for i in range(n):
#         t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
#         date_touple = time.localtime(t)  # 将时间戳生成时间元组
#         date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)  # 将时间元组转成格式化字符串（2020-04-11 16:33:21）
#         # print(date)
#
# def create_code(n):# order_num 15, purchase_time,
#     # id_num = ''
#     str = ''
#     for i in range(n):
#         value = random.choice(list2)
#         s = chr(value)
#         str += s
#     return str


def create_order():
    global start_time
    with open("Order.json", "w", encoding='utf-8') as f:
        f.write('[')
        for i in range(len(list_user_count)):
            account = list_user_count[i]
            begin = random.choice(list_begin)*7
            for j in range(30):
                gap = random.choice(list_gap)*7
                begint = start_time + datetime.timedelta(days=begin)
                endt = begint+datetime.timedelta(days=gap)
                a1 = tuple(begint.timetuple()[0:9])  # 设置开始日期时间元组
                a2 = tuple(endt.timetuple()[0:9])  # 设置结束日期时间元组

                start = time.mktime(a1)  # 生成开始时间戳
                end = time.mktime(a2)  # 生成结束时间戳

                # 随机生成日期字符串
                t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
                date_touple = time.localtime(t)  # 将时间戳生成时间元组
                date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)  # 将时间元组转成格式化字符串（2020-04-11 16:33:21）
                pay_amount = random.randint(1, 9999)
                msg = {
                    'order_number': md5(f'{account}'.encode(encoding='utf-8')).hexdigest()[:5]+md5(f'{pay_amount}'.encode(encoding='utf-8')).hexdigest()[:5]+md5(f'{date}'.encode(encoding='utf-8')).hexdigest()[:5],
                    'purchase_time': date,
                    'payment_amount': pay_amount,
                    'payment_method': random.choice(list3),
                    'status': random.choice(list4),
                    'user_account':account
                }
                if i+j != 0:
                    f.write(',')
                json.dump(msg, f)
                begin +=(gap+17)# 15+1+1
        f.write(']')
    return

def create_ticket():
    with open("Ticket.json", "w", encoding='utf-8') as f:
        f.write('[')
        # c转换为order list
        for i in range(len(a)):
            per_list = d_dict[a[i]['account']]
            order_list = c_dict[a[i]['account']]
            for k in range(len(order_list)):
                if order_list[k]['status'] != 'unpaid':
                    date_std = order_list[k]['purchase_time']
                    date_std_t = datetime.datetime.strptime(date_std, "%Y-%m-%d %H:%M:%S")
                    date_end_t = date_std_t+datetime.timedelta(days=15)
                    a1 = tuple(date_std_t.timetuple()[0:9])  # 设置开始日期时间元组
                    a2 = tuple(date_end_t.timetuple()[0:9])  # 设置结束日期时间元组

                    start = time.mktime(a1)  # 生成开始时间戳
                    end = time.mktime(a2)  # 生成结束时间戳

                    # 随机生成日期字符串
                    # t = random.randint(start, end)
                    # date_touple = time.localtime(t)  # 将时间戳生成时间元组
                    # date = time.strftime("%Y-%m-%d", date_touple)
                    order_number = order_list[k]['order_number']
                    for j in range(4):
                        t = random.randint(start, end)
                        date_touple = time.localtime(t)  # 将时间戳生成时间元组
                        date = time.strftime("%Y-%m-%d", date_touple)
                        id_number = per_list[j]
                        train_number = random.choice(e)['train_number']
                        dd = random.sample(g_dict[train_number],2)
                        dd.sort(key=lambda x:x["stop_order"])
                        d = dd[0]
                        dt =dd[1]
                        d_sta = d['station_name']
                        dt_sta = dt['station_name']
                        d_time = d['arrival_time']
                        dt_time = dt['arrival_time']
                        msg={
                            "ticket_number":md5(f'{train_number}'.encode(encoding='utf-8')).hexdigest()[:5]+md5(f'{id_number}'.encode(encoding='utf-8')).hexdigest()[:5]+md5(f'{order_number}'.encode(encoding='utf-8')).hexdigest()[:5]+md5(f'{date}'.encode(encoding='utf-8')).hexdigest()[:5],
                            "train_number":train_number,
                            "departure_station":d_sta,
                            "destination_station":dt_sta,
                            "fare":random.randint(1,9999),
                            "date":date,
                            "id_number":id_number,
                            "order_number":order_number,
                            "departure_time":d_time,
                            "arrival_time":dt_time
                        }
                        if i + j + k != 0:
                            f.write(',')
                        json.dump(msg, f)
        f.write(']')




with open("Ticket.json",'r',encoding='utf-8') as f:
    u = json.load(f)
with open("Train.json",'r',encoding='utf-8') as f:
    v = json.load(f)
#
def create_Seats():
    with open("Seats.json",'w',encoding='utf-8') as f:
        f.write('[')
        global start_time_2
        train_list = []
        for i in v:
            train_list.append(i['train_number'])
        train_day = collections.defaultdict(list)
        # time_end = start_time_2 + datetime.timedelta(days=15)
        for i in range(len(train_list)):
            for j in range(16):
                train_day[train_list[i]].append(1200)
        for i in range(len(u)):
            tmp = u[i]
            time = datetime.datetime.strptime(tmp['date'], "%Y-%m-%d").date()
            if (time-start_time_2.date()).days>-1 :
                train_num = tmp['train_number']
                # 计算天数
                day = (time-start_time_2.date()).days
                train_day[train_num][day] -=1

        for i in range(len(train_list)):
            for j in range(16):
                msg = {
                    "train_number":train_list[i],
                    "date":(start_time_2 + datetime.timedelta(days=j)).strftime("%Y-%m-%d"),
                    "remaining_seats":train_day[train_list[i]][j]
                }
                if i + j != 0:
                    f.write(',')
                json.dump(msg, f)
        f.write(']')
    return 0



#
def create_person_info():
    with open("Person_info.json", "w", encoding='utf-8') as f:
        f.write('[')
        sig_id = list_pas_id[:400000]
        mul_id = list_pas_id[400000:]
        for i in range(len(list_user_count)):
            for j in range(4):
                msg = {
                    "account":list_user_count[i],
                    "id_number":sig_id[4*i+j]
                }
                if i + j != 0:
                    f.write(',')
                json.dump(msg, f)
            tmp_id = random.sample(mul_id,6)
            for j in range(6):
                msg = {
                    "account": list_user_count[i],
                    "id_number": tmp_id[j]
                }
                f.write(',')
                json.dump(msg, f)
        f.write(']')

# print(len(a['user']))
if __name__=='__main__':
    create_person_info()
    create_order()
    create_ticket()
    create_Seats()
