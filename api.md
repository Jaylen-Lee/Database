# 接口文档


### 说明
- 端口号默认为8080，完整url地址为(http://localhost:8080/URL)
- 返回值暂时没有进行错误检查，如果后端处理失败时能统一返回一个标志，则可以在前端添加错误处理
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
  - `identity`:true = 学生

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
  - `identity`（乘客类型）:true = 学生
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
- **后端操作** 
    - 根据参数，查询并返回数据，注意返回值字段必须与下面一致
- **返回值[{item}]**  
  - `start_station`（起始站）
  - `arrive_station`（终点站）
  - `go_time`（出发时间）: hh:mm
  - `arrive_time`（到达时间）: hh:mm
  - `train_number`（列车号）
  - `price`（票价）: 
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

### 9.修改某一用户下的乘客信息
- **URL**
  - `./Passenger/modify`
- **方法**
  - `POST`
- **参数**
  - `account`（所属的用户账号）
  - `name`（乘客的姓名）
  - `phone`（乘客的联系电话）
  - `identity`（乘客身份）：true=学生
- **后端操作** 
  - 先修改个人信息表，然后同步到乘客表（也许还得再改一边个人信息表，因为可能存在几个用户添加同一乘客的情况？）
- **返回值**  
  - 无

### 10.删除某一用户下的乘客信息
- **URL**
  - `./Passenger/delete`
- **方法**
  - `POST`
- **参数**
  - `account`（所属的用户账号）
  - `id_number`（该乘客的身份证号）
- **后端操作** 
  - 先从个人信息表中删除，然后同步到乘客表（若不存在多个用户添加该乘客的情况，直接从乘客表中删除）
- **返回值[{item}]**  
  - 无

### 11.基于查询得到的车次信息购票

- **URL**

  - `./Ticket/choose`

- **方法**

  - `POST`

- **参数**

  - `account`（所属的用户账号）

  - `date`(所选车次的日期)

  - `train_number`(所选车次)

  -  `start_station`(以下四个为车次出发到达信息)

  - `arrive_station`

  - `start_time`

  - `arrive_time`

  - `paymentOptions`   固定格式，只会有一个checked为True即付款方式，paymentOptions: [

       { name: 'cash', checked: false },

       { name: 'wechat', checked: false },

       { name: 'alipay', checked: false }

      ]

  - `count`(购票数量，即下面两个list的长度，可以判断余票数量是否不小于count来返回购票结果)

  - `id_list`(需要购票的乘客的id列表)

  - `pay_method`（支付方式）

  - `identity_list`（需要购票的乘客的identity列表，1为学生，0为成人）

- **后端操作** 

  - 在seats表中检查对应余票是否充足，然后根据运行时间计算票价，学生票七五折，生成并存入unpaid订单，生成取票号等信息并存入ticket订单(座位数量不减少，等确认支付后再减少对应座位数量，这需要再写一个，后面补充）

- **返回值[{item}]**  

  - true/false 订单生成成功与否

### 12.付款与退款操作

- **URL**
  - ./Order/refund 或 ./Order/completed
- **方法**
  - POST
- **参数**
  - order_number 
- **后端操作** 
  - 修改订单状态为refund或者completed
- **返回值[{item}]**  
  - true/false 不过false的情况没有定义

### 13.查询订单下的车票

- **URL**
  - ./Ticket/findbyId
- **方法**
  - POST
- **参数**
  - order_number
- **后端操作** 
  - 根据order_number查询车票信息
- **返回值[{item}]**  
  - list形式返回所属车票的全部信息


### 14.查询某一用户的所有订单信息
- **URL**
  - `./Order/findbyaccount`
- **方法**
  - `GET`
- **参数**
  - `account`（用户账号）
- **后端操作** 
  - 查询订单表，返回该用户的所有订单信息
- **返回值[{item}]**  
  - `order_number`（订单号）
  - `purchase_time`（下单时间）
  - `payment_amount`（支付金额）
  - `payment_method`（支付方式）
  - `status`（订单状态）
  - `user_account`（用户账号）

### 15.管理员查询某一车次的信息
- **URL**
  - `./Train/findbyid`
- **方法**
  - `GET`
- **参数**
  - `train_number`
- **后端操作** 
  - 联合车次表和到达时间表，返回需要的信息即可
- **返回值[{item}]**  
  - `train_number`（车次编号）
  - `station_name`（当前到达车站名）
  - `arrival_time`（当前车站的到达时间）
  - `stop_order`（停靠顺序编号）
  - `seats_num` （该车次的座位数） 
  - `mileage`（该车次的总里程）
  - `train_type`（类型，普快等）
### 16.管理员查询用户信息（模糊匹配）
- **URL**
  - `./Ad/finduser`
- **方法**
  - `GET`
- **参数**
  - `account`（模糊账号）
- **后端操作** 
  - 对用户表进行模糊查询，返回用户信息
- **返回值[{item}]** 
  - `account`
  - `username`
  - `password`
  - `noOfOrder`
