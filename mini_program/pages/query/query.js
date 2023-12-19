// pages/quary/quary.js
var util = require('../../utils/util.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    trival_List: [{depareture_station : '上海',
    arrival_station : '北京西',
    depareture_time: 'hh:mm',
    arrival_time : 'hh:mm',
    train_number: 'E568',
    fare : '333',
    date: 'yyyy-mm-dd',
    remain: '1199'}],
    hidden: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var self = this
    wx.request({
      url: 'http://localhost:8080/Train/query',
      data: {
        start_station: wx.getStorageSync('startName'),
        arrive_station: wx.getStorageSync('endName'),
        go_date: wx.getStorageSync('year') + wx.getStorageSync('month') + '-' + wx.getStorageSync('day'),
        // type: (wx.getStorageSync('stu_ticket') ? '学生票' : '成人票')
      },
      success: function(res) {

        for (var i = 0; i < res.data.length; i++) {
          var start = "ticketList[" + i + "].start_station"
          var end = "ticketList[" + i + "].arrive_station"
          var go_time = "ticketList[" + i + "].go_time"
          var arrive_time = "ticketList[" + i + "].arrive_time"
          var train_number = "ticketList[" + i + "].train_number"
          // var seat_type = "ticketList[" + i + "].seat_type"
          var type = "ticketList[" + i + "].type"
          var price = "ticketList[" + i + "].price"
          // var ticket_id = "ticketList[" + i + "].ticket_id"
          var ticket_goDate = "ticketList[" + i + "].go_date"
          var remain = "ticketList[" + i + "].remain"

          self.setData({
            [go_time]: res.data[i].go_time.toString().substring(0, 5),
            [arrive_time]: util.formatTime(new Date(res.data[i].arrive_time)).split(' ')[1].substring(0, 5),
            [start]: res.data[i].start_station,
            [end]: res.data[i].arrive_station,
            [train_number]: res.data[i].train_number,
            [price]: res.data[i].price,
            // [seat_type]: res.data[i].seat_type,
            [type]: res.data[i].type,
            // [ticket_id]: res.data[i].ticket_id,
            [ticket_goDate]: res.data[i].go_date.toString(),
            [remain]: res.data[i].remain

          })
          
          // 跨天时，标识"+1"
          if (res.data[i].go_date.toString().replace(/-/g, '') < util.formatTime(new Date(res.data[i].arrive_time)).split(' ')[0].replace(/\//g, '')) {
            self.setData({
              hidden: false
            })
          } else {
            self.setData({
              hidden: true
            })
          }

        }
      }
    })

  },

  buyTicket: function(e) {
    wx.navigateTo({
      url: '../choose_passenger/choose_passenger',
    })
    // wx.setStorageSync('ticket_id', e.currentTarget.dataset.ticketId)
    wx.setStorageSync('go_date', e.currentTarget.dataset.goDate)
    wx.setStorageSync('train_number', e.currentTarget.dataset.trainNumber)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})