import pandas as pd
import numpy as np
import json



def create_arrival_time():
    # pass
    data1 = pd.read_excel('高铁列车信息(1).xlsx')
    # data2 = pd.read_excel('高铁线路信息.xlsx')
    data1 = data1.drop([0])
    train_code = np.unique(data1['Trnub'].tolist())
    with open("Arrival_time.json", "w", encoding='utf-8') as f:
        f.write('[')
        for i in train_code:
            data_tmp = data1[data1['Trnub'] == i]
            data_tmp.sort_values(by=['Mileage'],ascending=[True])
            # print(data_tmp['Mileage'].tolist())
            # 重排序
            for j in range(len(data_tmp)):
                msg = {
                    'train_number': i,
                    'station_name': data_tmp['Dptstt'].tolist()[j],
                    'arrival_time': data_tmp['Dpttm'].tolist()[j],
                    # 'stop_time':,
                    'stop_order':j
                }
                # if i+j!=0 :
                f.write(',')
                json.dump(msg, f)
            # if i % 10000 == 0:
            #     print(i)
            msg = {
                'train_number': i,
                'station_name': data_tmp['Arvstt'].tolist()[0],
                'arrival_time': data_tmp['Arvtm'].tolist()[0],
                # 'stop_time':,
                'stop_order': len(data_tmp)
            }
            f.write(',')
            json.dump(msg, f)
        f.write(']')

def create_station():
    data2 = pd.read_excel('高铁站开通时间.xlsx')
    print(data2['Hsrwsnm'].tolist()[0])
    data2 = data2.drop([0])
    print(data2['Hsrwsnm'].tolist()[0])
    # data2.drop([0])
    # print(data2['Hsrwsnm'].tolist()[0])
    train_code = np.unique(data2['Hsrwsnm'].tolist())
    with open("Station.json", "w", encoding='utf-8') as f:
        f.write('[')
        for i in enumerate(train_code):
            data_tmp = data2[data2['Hsrwsnm']==i]
            # 注意是数字还是字符串
            msg={
                'station_name': i,
                'address': data_tmp['Prvn'].tolist()[0]+data_tmp['Ctynm'].tolist()[0],
                'opening_time': data_tmp['Optm'].tolist()[0]
            }
            if i!=0:
                f.write(',')
            json.dump(msg, f)
        f.write(']')

def create_train(): # train_number v15,seat_num 200-5000; train_type v10; mileage; route v10
    seat_num = 1200
    data1 = pd.read_excel('高铁列车信息(1).xlsx')
    data2 = pd.read_excel('高铁线路信息.xlsx')
    data1 = data1.drop([0])
    train_code = np.unique(data1['Trnub'].tolist())
    with open("Train.json", "w", encoding='utf-8') as f:
        f.write('[')
        for i in train_code:
            data_tmp = data1[data1['Trnub']==i]
            # 注意是数字还是字符串
            msg={
                'train_number': i,
                'seats_num': 1200,
                'train_type': data_tmp['Models'].tolist()[0],
                'mileage': max(data_tmp['Mileage'].tolist())#求最大值
                # 'affiliated_route':
            }
            if i!=0:
                f.write(',')
            json.dump(msg, f)
            # if i % 10000 == 0:
            #     print(i)
        f.write(']')

if __name__=='__main__':
    create_train()
    create_arrival_time()
    create_station()







