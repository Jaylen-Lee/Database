# 接口文档


### 说明
- 端口号默认为8080，完整url地址为(http://localhost:8080/URL)
- **URL**
  - 
- **方法**
  - 
- **参数**
  - 
- **后端操作** 
  - 
- **返回值[{item}]**  
  - 


### 1.用户注册
- **URL**
  - `./User/register`
- **方法**
  - `POST`
- **参数**
  - `account`（用户账号）：由用户自己指定，在前端进行重复检查，保证送给后端的账号不重复
  - `username`（用户名）：不用进行重复检查
  - `passward`（密码）：不进行安全等级检查
- **后端操作** 
  - 新用户信息插入数据库 
- **返回值**
  - 无

### 2.查询用户已添加的乘客
- **URL**
  - `./Passenger/findbyuser`
- **方法**
  - `POST`
- **参数**
  - `account`（用户账号）
- **后端操作** 
  - 返回该用户已添加的所有乘客
- **返回值[{item}]**  
  - `name`
  - `id_number`
  - `phone`
  - `identity`

### 3.添加乘客
- **URL**
  - `./Passenger/add`
- **方法**
  - `POST`
- **参数**
  - `account`（用户账号）
  - `id_number`（乘客身份证号）
  - `name`（乘客姓名）
  - `phone`（乘客电话号）
  - `indentity`（乘客类型）
- **后端操作** 
  - 将新的乘客信息添加到个人信息表中，并同步到乘客表
- **返回值**  
  - 若已经存在该乘客，返回fasle

### 4.查询所有用户账号
- **URL**
  - `/User/findall_account`
- **方法**
  - `GET`
- **参数**
  - 无
- **后端操作** 
  - 查询所有的账号，包括用户表和管理员表
- **返回值[item]**  
  - `item`（账号）：应保证所有的账号不重复

### 5.根据特定账号查找用户/管理员信息
- **URL**
  - `./User/findby_account`
- **方法**
  - `GET`
- **参数**
  - `is_ad`（是否为管理员）：true = 是管理员
  - `account`（用户账号）
- **后端操作** 
  - 根据参数is_ad，决定在管理员表/用户表中按照account查找对应的信息
- **返回值{item}**  
  - `account`:
  - `username`:
  - `name`: 若为用户，返回空字符串
  - `passward`:
  - `phone`:  若为用户，返回空字符串

### 6. 查询车站名
- **URL**
  - `./Station/findall`
- **方法**
  - `GET`
- **参数**
  - 无
- **后端操作** 
  - 从车站表中查询所有的车站名
- **返回值[item]**  
  - `station_name`

### 7. 查询车次信息

- **URL**
  - `./Train/query`
- **方法**
  - `GET`
- **参数**
    - `start_station` （出发站） 
    - `arrive_station` （终点站）    
    - `go_date` （出发日期）: yyyy-mm-dd
    - `type` （身份类型）: 学生票/成人票
- **后端操作** 
    - 根据参数，查询并返回数据，注意返回值字段必须与下面一致
- **返回值[{item}]**  
  - `start_station`（起始站）
  - `arrive_station`（终点站）
  - `go_time`（出发时间）: hh:mm
  - `arrive_time`（到达时间）: hh:mm
  - `train_number`（列车号）
  - `type`（票类型）：成人票/学生票
  - `price`（票价）: 若为学生票，应乘0.75 
  - `go_date`（出发日期）：yyyy-mm-dd
  - `remain`（剩余票数）

### 8.修改用户/管理员信息
- **URL**
  - `./User/modify`
- **方法**
  - `POST`
- **参数**
  - `is_ad`（是否为管理员）：true = 是管理员
  - `account`（账号）:
  - `username`（用户名）:
  - `name`: 若为用户，则没有该字段
  - `passward`:
  - `phone`:  若为用户，则没有该字段
- **后端操作** 
  - 根据`is_ad`，决定在用户表/管理员表中更新信息
- **返回值**  
  - 无