//index.js
//获取应用实例
var app = getApp()

var timestamp = Date.parse("2023-06-17");
var date = new Date(timestamp);
console.log(date)
Page({
  data: {
    is_ad : false,
    year : date.getFullYear(),
    month: ('0' + (date.getMonth() + 1)).slice(-2),
    day: ('0' + date.getDate()).slice(-2), 
    current_date: "2023-06-17",
    end_date: "2023-07-02",
    startName: '出发站',
    endName: '目的站',
    stu_ticket: false
  },

  stu_ticket_choose: function (e) {
    wx.setStorageSync('stu_ticket', e.detail.value)
    this.setData({
      stu_ticket: e.detail.value
    })
  },

  gotoStart: function () {
    wx.navigateTo({
      url: '../start/start'
    })
  },

  gotoDestination: function () {
    wx.navigateTo({
      url: '../destination/destination'
    })
  },

  gotoQuery: function () {
    if (this.data.startName == this.data.endName) {
      wx.showModal({
        title: '温馨提示',
        content: '不能选择相同的出发站点和目的站点，请重新选择',
        showCancel: false
      })
    } else {
      wx.navigateTo({
        url: '../query/query'
      })
    }
  },

  onLoad: function () {


    // 优先使用缓存的出发站和到达站
    var name1 = wx.getStorageSync('startName');
    if (name1) {
      this.setData({
        startName: name1
      });
    }
    var name2 = wx.getStorageSync('endName');
    if (name2) {
      this.setData({
        endName: name2
      });
    }
    // 动态决定查询日期范围
    /*let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth() + 1; // 月份是从 0 开始的，所以需要加 1
    let day = today.getDate();*/

    // 格式化初始日期，例如：2023-09-01
    /*let formattedDate = `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`;*/

    // 计算结束日期，假设要设置为初始日期的三个月后
    /*let endMonth = month + 3;
    let endYear = year + Math.floor(endMonth / 12);
    endMonth = endMonth % 12 || 12;*/

    /*let formattedEndDate = `${endYear}-${endMonth < 10 ? '0' + endMonth : endMonth}-${day < 10 ? '0' + day : day}`;
    this.setData({
      current_date : formattedDate,
      end_date : formattedEndDate
    })*/
    // 如果存在缓存的日期，应重置为当前日期
    var m = wx.getStorageSync("month")
    var d = wx.getStorageSync("day")
    if (m && d) {
      this.setData({
        month: ('0' + (date.getMonth() + 1)).slice(-2),
        day: ('0' + date.getDate()).slice(-2)
      })
      wx.setStorageSync('month', this.data.month)
      wx.setStorageSync('day', this.data.day)
    }
    console.log(this.data.day)
    wx.setStorageSync('stu_ticket', this.data.stu_ticket)
  },

  onShow: function (e) {
    if(wx.getStorageSync('is_ad')){
      this.setData({is_ad:true})
    }
    var name1 = wx.getStorageSync('startName');
    if (name1) {
      this.setData({
        startName: name1
      });
    }
    var name2 = wx.getStorageSync('endName');
    if (name2) {
      this.setData({
        endName: name2
      });
    }
    var m = wx.getStorageSync('month')
    var d = wx.getStorageSync('day')
    if (m && d) {
      this.setData({
        month: m,
        day: d
      })
    }
  },

  switch: function () {
    var name1 = wx.getStorageSync('startName');
    var name2 = wx.getStorageSync('endName');
    if (name1 && name2) {
      this.setData({
        startName: name2,
        endName: name1,
      })

      wx.setStorageSync('startName', name2)
      wx.setStorageSync('endName', name1)
    }
  },
  bindDateChange(e) {
    const selectedDate = e.detail.value;
    // 将选择的日期字符串转换为 Date 对象
    const selectedDateObject = new Date(selectedDate);
    // 获取月份和日期
    const selectedYear = selectedDateObject.getFullYear();
    const selectedMonth = ('0' + (selectedDateObject.getMonth() + 1)).slice(-2);// 月份是从 0 开始的，所以需要加 1
    const selectedDay = ('0' + selectedDateObject.getDate()).slice(-2);
    this.setData({
        year : selectedYear,
        month : selectedMonth,
        day : selectedDay
    });
    wx.setStorageSync('year', selectedYear),
    wx.setStorageSync('month', selectedMonth),
    wx.setStorageSync('day', selectedDay)
    //console.log(wx.getStorageSync('year'))
  },
})